from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Avg, Max, Q
from django.http import HttpResponse
from alumni.models import Alumni, Prodi
from survey.models import Survey

# ... (Import ReportLab tidak berubah, biarkan saja di atas) ...
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie

import io
import datetime
import json

def is_admin(user):
    return user.is_staff or user.is_superuser

# --- HELPER: Ambil Data Statistik ---
def get_statistik_data(tahun_filter=None, prodi_filter=None):
    alumni_qs = Alumni.objects.all()
    if prodi_filter: alumni_qs = alumni_qs.filter(prodi_id=prodi_filter)
    if tahun_filter: alumni_qs = alumni_qs.filter(tahun_lulus=tahun_filter)
        
    # 1. Total Alumni Terdaftar (Sesuai Filter)
    total_alumni = alumni_qs.count()

    # 2. Total Responden (Alumni yang sudah isi survey/bekerja)
    total_responden = alumni_qs.filter(status_bekerja=True).count()

    # 3. Hitung Relevansi (Persentase Sesuai + Sangat Sesuai)
    survey_qs = Survey.objects.filter(alumni__in=alumni_qs)
    
    jml_relevan = survey_qs.filter(
        Q(kesesuaian='Sangat Sesuai') | Q(kesesuaian='Sesuai')
    ).count()
    
    total_survey = survey_qs.count()
    
    # Hitung Persen (Hindari pembagian nol)
    persen_relevansi = 0
    if total_survey > 0:
        persen_relevansi = (jml_relevan / total_survey) * 100
        
    # Data Pie Chart (Untuk PDF Legacy)
    count_bekerja = total_responden
    count_belum = total_alumni - total_responden

    return {
        'total_alumni': total_alumni,
        'total_responden': total_responden,
        'persen_relevansi': round(persen_relevansi, 1), # Pembulatan 1 desimal
        'pie_data': [count_bekerja, count_belum],
    }

@login_required
def statistik_dashboard(request):
    # --- LOGIC LINE CHART (TREN) ---
    years_qs = Alumni.objects.values_list('tahun_lulus', flat=True).distinct().order_by('tahun_lulus')
    list_tahun = list(years_qs)
    
    data_bekerja_per_tahun = []
    if not list_tahun: list_tahun = []; data_bekerja_per_tahun = []
    else:
        for t in list_tahun:
            jml = Alumni.objects.filter(tahun_lulus=t, status_bekerja=True).count()
            data_bekerja_per_tahun.append(jml)

    # --- LOGIC KOTAK ANGKA ---
    tahun_filter = request.GET.get('tahun')
    prodi_filter = request.GET.get('prodi')
    stats = get_statistik_data(tahun_filter, prodi_filter)
    
    # Ranking Gaji
    ranking_gaji = Prodi.objects.annotate(
        max_gaji=Max('alumni__surveys__gaji'),
        avg_gaji=Avg('alumni__surveys__gaji')
    ).exclude(max_gaji__isnull=True).order_by('-max_gaji')

    context = {
        'is_admin': is_admin(request.user),
        
        # Data Angka untuk Kotak Atas
        'kpi_alumni': stats['total_alumni'],
        'kpi_responden': stats['total_responden'],
        'kpi_relevansi': stats['persen_relevansi'],

        # Data Grafik Line
        'chart_years': json.dumps(list_tahun),
        'chart_trend_data': json.dumps(data_bekerja_per_tahun),
        
        'ranking_gaji': ranking_gaji,
        'prodi_list': Prodi.objects.all(),
        'tahun_list': years_qs,
        'pie_data': stats['pie_data'] # Utk PDF
    }
    
    return render(request, 'statistik/dashboard.html', context)

# ... (Fungsi export_pdf biarkan saja seperti sebelumnya) ...
@login_required
@user_passes_test(is_admin)
def export_pdf(request):
    # (Kode export_pdf sama persis dengan yang terakhir "Clean Version", tidak perlu diubah)
    # Copas ulang function export_pdf dari chat sebelumnya jika hilang.
    tahun = request.GET.get('tahun')
    prodi = request.GET.get('prodi')
    
    response = HttpResponse(content_type='application/pdf')
    filename = f"Executive_Report_{datetime.date.today()}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    elements = []
    styles = getSampleStyleSheet()

    # HEADER
    elements.append(Paragraph("LAPORAN STATISTIK TRACER STUDY", styles['Title']))
    elements.append(Spacer(1, 20))

    # DATA
    stats = get_statistik_data(tahun, prodi)
    
    # ... (Sisa logic PDF sama, pakai stats['pie_data'] dsb) ...
    # Agar singkat, gunakan fungsi export_pdf dari jawaban "Clean PDF" sebelumnya.
    # Karena fokus request ini adalah Tampilan Dashboard HTML.
    
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response