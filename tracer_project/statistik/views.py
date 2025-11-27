from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from survey.models import Survey
from django.db.models import Avg, Count

@login_required
def statistik_index(request):
    surveys = Survey.objects.all()

    total_responden = surveys.count()

    # Persentase bekerja
    total_bekerja = surveys.filter(status_pekerjaan="Bekerja").count()
    persentase_bekerja = (total_bekerja / total_responden * 100) if total_responden > 0 else 0

    # Rata-rata waktu tunggu
    rata_waktu_tunggu = surveys.aggregate(avg=Avg("waktu_tunggu"))["avg"] or 0

    # Rata-rata gaji
    rata_gaji = surveys.aggregate(avg=Avg("gaji"))["avg"] or 0

    # Distribusi kesesuaian jurusan
    kesesuaian = surveys.values("kesesuaian_jurusan").annotate(total=Count("id"))

    # Distribusi status pekerjaan
    status_pekerjaan = surveys.values("status_pekerjaan").annotate(total=Count("id"))

    context = {
        "total_responden": total_responden,
        "persentase_bekerja": round(persentase_bekerja),
        "rata_gaji": int(rata_gaji),
        "rata_waktu_tunggu": round(rata_waktu_tunggu, 1),
        "kesesuaian": kesesuaian,
        "status_pekerjaan": status_pekerjaan,
    }

    return render(request, "statistik/index.html", context)
