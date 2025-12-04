from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Avg, Max
from django.http import HttpResponse
from alumni.models import Alumni, Prodi
from survey.models import Survey

# --- LIBRARY PDF REPORTLAB (LENGKAP) ---
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.legends import Legend

import io
import datetime
import json

def is_admin(user):
    return user.is_staff or user.is_superuser

# --- HELPER: Ambil Data Statistik (Sama seperti sebelumnya) ---
def get_statistik_data(tahun_filter=None, prodi_filter=None):
    alumni_qs = Alumni.objects.all()
    if prodi_filter:
        alumni_qs = alumni_qs.filter(prodi_id=prodi_filter)
    if tahun_filter:
        alumni_qs = alumni_qs.filter(tahun_lulus=tahun_filter)
        
    # 1. Status Bekerja
    stats_bekerja = alumni_qs.values('status_bekerja').annotate(total=Count('id'))
    count_bekerja = 0
    count_belum = 0
    for item in stats_bekerja:
        if item['status_bekerja']: count_bekerja = item['total']
        else: count_belum = item['total']

    # 2. Kesesuaian
    survey_qs = Survey.objects.filter(alumni__in=alumni_qs)
    stats_kesesuaian = survey_qs.values('kesesuaian').annotate(total=Count('id')).order_by('-total')
    
    label_kesesuaian = [item['kesesuaian'] for item in stats_kesesuaian]
    data_kesesuaian = [item['total'] for item in stats_kesesuaian]
    
    # Hitung Avg Gaji untuk Summary
    avg_gaji = survey_qs.aggregate(Avg('gaji'))['gaji__avg'] or 0
    
    return {
        'pie_data': [count_bekerja, count_belum],
        'label_kesesuaian': label_kesesuaian,
        'data_kesesuaian': data_kesesuaian,
        'total_responden': count_bekerja + count_belum,
        'avg_gaji': avg_gaji
    }

@login_required
def statistik_dashboard(request):
    # ... (LOGIC DASHBOARD VIEW TETAP SAMA SEPERTI YANG SUDAH FIXED TADI) ...
    # ... (Silakan copy bagian statistik_dashboard dari jawaban sebelumnya jika tertimpa) ...
    # ... (Tapi karena fokus kita PDF, saya tulis ulang logic PDF-nya saja di bawah) ...
    
    # SUPAYA KODE LENGKAP, SAYA TULIS ULANG FULL DASHBOARDNYA:
    years_qs = Alumni.objects.values_list('tahun_lulus', flat=True).distinct().order_by('tahun_lulus')
    list_tahun = list(years_qs)
    data_bekerja_per_tahun = []
    if not list_tahun: list_tahun = []; data_bekerja_per_tahun = []
    else:
        for t in list_tahun:
            jml = Alumni.objects.filter(tahun_lulus=t, status_bekerja=True).count()
            data_bekerja_per_tahun.append(jml)

    tahun_filter = request.GET.get('tahun')
    prodi_filter = request.GET.get('prodi')
    stats = get_statistik_data(tahun_filter, prodi_filter)
    
    ranking_gaji = Prodi.objects.annotate(
        max_gaji=Max('alumni__surveys__gaji'),
        avg_gaji=Avg('alumni__surveys__gaji')
    ).exclude(max_gaji__isnull=True).order_by('-max_gaji')

    context = {
        'is_admin': is_admin(request.user),
        'chart_years': json.dumps(list_tahun),
        'chart_trend_data': json.dumps(data_bekerja_per_tahun),
        'chart_label_kesesuaian': json.dumps(stats['label_kesesuaian']),
        'chart_data_kesesuaian': json.dumps(stats['data_kesesuaian']),
        'ranking_gaji': ranking_gaji,
        'prodi_list': Prodi.objects.all(),
        'tahun_list': years_qs,
        'pie_data': stats['pie_data']
    }
    return render(request, 'statistik/dashboard.html', context)

# ==========================================================
# BAGIAN PDF YANG DI-UPGRADE TOTAL (PREMIUM LOOK)
# ==========================================================
@login_required
@user_passes_test(is_admin)
def export_pdf(request):
    tahun = request.GET.get('tahun')
    prodi_id = request.GET.get('prodi')
    
    # Ambil Nama Prodi
    nama_prodi = "Semua Program Studi"
    if prodi_id:
        try:
            nama_prodi = Prodi.objects.get(id=prodi_id).nama
        except: pass

    # Setup Dokumen
    response = HttpResponse(content_type='application/pdf')
    filename = f"Executive_Report_{datetime.date.today()}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Styles
    title_style = ParagraphStyle('TitleCustom', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor('#2c3e50'), alignment=TA_CENTER, spaceAfter=10)
    subtitle_style = ParagraphStyle('SubtitleCustom', parent=styles['Normal'], fontSize=12, textColor=colors.HexColor('#7f8c8d'), alignment=TA_CENTER, spaceAfter=30)
    h2_style = ParagraphStyle('H2Custom', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#2980b9'), spaceBefore=20, spaceAfter=10)
    
    # --- HEADER ---
    elements.append(Paragraph("LAPORAN EKSEKUTIF TRACER STUDY", title_style))
    info_filter = f"{nama_prodi} | Tahun Lulus: {tahun or 'Semua Angkatan'}"
    elements.append(Paragraph(f"Periode Laporan: {datetime.date.today().strftime('%d %B %Y')}<br/>{info_filter}", subtitle_style))

    # Ambil Data
    stats = get_statistik_data(tahun, prodi_id)

    # --- SUMMARY KOTAK ANGKA ---
    total_resp = stats['total_responden']
    persen_kerja = (stats['pie_data'][0] / total_resp * 100) if total_resp > 0 else 0
    
    data_summary = [
        ['TOTAL ALUMNI', 'TINGKAT KETERSERAPAN', 'RATA-RATA GAJI'],
        [f"{total_resp}", f"{persen_kerja:.1f}%", f"Rp {stats['avg_gaji']:,.0f}"]
    ]
    
    t_summary = Table(data_summary, colWidths=[2.3*inch, 2.3*inch, 2.3*inch])
    t_summary.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('TEXTCOLOR', (0,0), (-1,0), colors.gray),
        ('FONTNAME', (0,1), (-1,1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,1), (-1,1), 20),
        ('TEXTCOLOR', (0,1), (0,1), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (1,1), (1,1), colors.HexColor('#27ae60')),
        ('TEXTCOLOR', (2,1), (2,1), colors.HexColor('#2980b9')),
        ('TOPPADDING', (0,1), (-1,1), 6),
        # HAPUS BOX DISINI BIAR CLEAN
        ('LINEAFTER', (0,0), (0,1), 1, colors.lightgrey),
        ('LINEAFTER', (1,0), (1,1), 1, colors.lightgrey),
    ]))
    elements.append(t_summary)
    elements.append(Spacer(1, 30))

    # --- GRAFIK (Pie & Bar) ---
    elements.append(Paragraph("A. Analisis Visual", h2_style))
    
    d_pie = Drawing(250, 150)
    pc = Pie()
    pc.x = 65
    pc.y = 15
    pc.width = 120
    pc.height = 120
    pc.data = stats['pie_data']
    pc.labels = ['Bekerja', 'Belum']
    pc.slices[0].fillColor = colors.HexColor('#2ecc71')
    pc.slices[1].fillColor = colors.HexColor('#e74c3c')
    
    leg_pie = Legend()
    leg_pie.x = 200
    leg_pie.y = 100
    leg_pie.colorNamePairs = [(colors.HexColor('#2ecc71'), 'Bekerja'), (colors.HexColor('#e74c3c'), 'Belum')]
    leg_pie.fontSize = 10
    d_pie.add(pc)
    d_pie.add(leg_pie)

    d_bar = Drawing(250, 150)
    bc = VerticalBarChart()
    bc.x = 30
    bc.y = 20
    bc.height = 110
    bc.width = 200
    if stats['data_kesesuaian']:
        bc.data = [stats['data_kesesuaian']]
        bc.categoryAxis.categoryNames = [x[:10] for x in stats['label_kesesuaian']]
        bc.bars[0].fillColor = colors.HexColor('#3498db')
        bc.valueAxis.valueMin = 0
    else:
        bc.data = [[0]]
    d_bar.add(bc)

    chart_table = Table([[d_pie, d_bar]], colWidths=[3.5*inch, 3.5*inch])
    chart_table.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    elements.append(chart_table)
    
    elements.append(Paragraph("Distribusi Status Pekerjaan & Tingkat Kesesuaian Studi", 
                              ParagraphStyle('caption', parent=styles['Normal'], fontSize=9, alignment=TA_CENTER, textColor=colors.gray)))
    elements.append(Spacer(1, 25))

    # --- TABEL DATA UTAMA (CLEAN VERSION) ---
    elements.append(Paragraph("B. Data Survey Terbaru (Top 30)", h2_style))
    
    data_rows = [['Nama Alumni', 'Perusahaan', 'Posisi', 'Gaji', 'Kesesuaian']]
    
    surveys = Survey.objects.select_related('alumni').all()
    if prodi_id: surveys = surveys.filter(alumni__prodi_id=prodi_id)
    if tahun: surveys = surveys.filter(alumni__tahun_lulus=tahun)
    surveys = surveys.order_by('-created_at')[:30]
    
    for s in surveys:
        gaji_str = f"Rp {s.gaji:,.0f}" if s.gaji else "-"
        nama = (s.alumni.nama[:20] + '..') if len(s.alumni.nama) > 20 else s.alumni.nama
        pt = (s.perusahaan[:20] + '..') if len(s.perusahaan) > 20 else s.perusahaan
        data_rows.append([nama, pt, s.bidang_pekerjaan, gaji_str, s.kesesuaian])

    t_data = Table(data_rows, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.2*inch, 1.2*inch])
    
    # === STYLE TABEL YANG BERSIH (NO GRID, NO ZEBRA) ===
    t_data.setStyle(TableStyle([
        # Header Style (Solid Blue, Clean)
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,0), 10),
        ('TOPPADDING', (0,0), (-1,0), 10),
        
        # Body Style (Polos)
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 9),
        ('ALIGN', (3,1), (3,-1), 'RIGHT'), # Gaji rata kanan
        ('ALIGN', (0,1), (2,-1), 'LEFT'),  # Teks rata kiri
        
        # HILANGKAN GRID KOTAK-KOTAK
        # Cuma pakai garis bawah tipis per baris biar mata enak baca
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#ecf0f1')),
    ]))
    elements.append(t_data)
    
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"* Data ditampilkan terbatas 30 entri terbaru.", 
                              ParagraphStyle('small', parent=styles['Normal'], fontSize=8, textColor=colors.gray)))

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response