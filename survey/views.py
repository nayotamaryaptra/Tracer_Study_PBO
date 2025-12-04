from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Survey
from .forms import SurveyForm
from alumni.models import Prodi, Alumni

# Helper
def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
def survey_list(request):
    # LOGIC ADMIN (View All + Filter)
    if request.user.is_staff:
        surveys = Survey.objects.select_related('alumni', 'alumni__prodi').all()
        
        # Filter Admin
        jurusan_id = request.GET.get('jurusan') # Fakultas
        prodi_id = request.GET.get('prodi')
        tahun = request.GET.get('tahun')

        if jurusan_id:
            surveys = surveys.filter(alumni__fakultas_id=jurusan_id)
        if prodi_id:
            surveys = surveys.filter(alumni__prodi_id=prodi_id)
        if tahun:
            surveys = surveys.filter(alumni__tahun_lulus=tahun)

        # Context khusus admin
        context = {
            'surveys': surveys,
            'is_admin': True,
            'prodi_list': Prodi.objects.all(),
            'tahun_list': Alumni.objects.values_list('tahun_lulus', flat=True).distinct(),
        }
        return render(request, 'survey/survey_list.html', context)

    # LOGIC MAHASISWA (My Data + CRUD Button)
    else:
        # Cek profil
        if not hasattr(request.user, 'alumni'):
            return redirect('dashboard')
            
        surveys = Survey.objects.filter(alumni=request.user.alumni)
        return render(request, 'survey/survey_list.html', {'surveys': surveys, 'is_admin': False})
@login_required
def survey_create(request):
    # Hanya untuk Alumni
    if is_admin(request.user):
        messages.error(request, "Admin harap menggunakan Admin Panel / tidak mengisi survey.")
        return redirect('survey:list')

    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            survey = form.save(commit=False)
            survey.alumni = request.user.alumni
            survey.save()
            messages.success(request, "Riwayat pekerjaan berhasil ditambahkan.")
            return redirect('survey:list')
    else:
        form = SurveyForm()
    return render(request, 'survey/survey_form.html', {'form': form, 'title': 'Tambah Pekerjaan'})

@login_required
def survey_edit(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    
    # Security: Cek kepemilikan
    if not is_admin(request.user) and survey.alumni.user != request.user:
        messages.error(request, "Anda tidak berhak mengedit data ini.")
        return redirect('survey:list')

    # Admin tidak boleh edit (sesuai rules), hanya delete. Tapi Alumni boleh edit.
    if is_admin(request.user):
        messages.warning(request, "Admin tidak diperbolehkan mengedit survey User.")
        return redirect('survey:list')

    if request.method == 'POST':
        form = SurveyForm(request.POST, instance=survey)
        if form.is_valid():
            form.save()
            messages.success(request, "Data berhasil diperbarui.")
            return redirect('survey:list')
    else:
        form = SurveyForm(instance=survey)
    return render(request, 'survey/survey_form.html', {'form': form, 'title': 'Edit Pekerjaan'})

@login_required
def survey_delete(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    
    # Admin Boleh Delete, Owner Boleh Delete
    if not is_admin(request.user) and survey.alumni.user != request.user:
        messages.error(request, "Akses ditolak.")
        return redirect('survey:list')

    if request.method == 'POST':
        survey.delete()
        messages.success(request, "Data dihapus.")
        return redirect('survey:list')
    
    return render(request, 'survey/survey_confirm_delete.html', {'object': survey})