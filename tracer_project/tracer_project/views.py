from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from alumni.models import Alumni
from survey.models import Survey
from feedback.models import Feedback
from django.db.models import Count, Avg

def login_page(request):
    if request.user.is_authenticated:
        return redirect('alumni_list')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('alumni_list')
        else:
            messages.error(request, 'Username atau password salah!')

    return render(request, 'login.html')

@login_required
def dashboard(request):
    # Hitung data
    total_alumni = Alumni.objects.count()
    total_survey = Survey.objects.count()
    total_feedback = Feedback.objects.count()

    bekerja = Survey.objects.filter(status_pekerjaan="Bekerja").count()
    persentase_bekerja = (bekerja / total_survey * 100) if total_survey > 0 else 0

    rata_gaji = Survey.objects.aggregate(avg=Avg("gaji"))["avg"] or 0

    context = {
        "total_alumni": total_alumni,
        "total_survey": total_survey,
        "total_feedback": total_feedback,
        "persentase_bekerja": round(persentase_bekerja),
        "rata_gaji": int(rata_gaji),
    }

    return render(request, "dashboard.html", context)
