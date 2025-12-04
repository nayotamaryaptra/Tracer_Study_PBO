# alumni/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.contrib import messages
from .models import Alumni, Prodi, Fakultas
from .forms import AlumniForm

# Helper check admin
def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
def alumni_list(request):
    # LOGIC MAHASISWA (Hanya View Profil)
    if not request.user.is_staff:
        try:
            profil = request.user.alumni
            return render(request, 'alumni/alumni_profile.html', {'alumni': profil})
        except Alumni.DoesNotExist:
            return render(request, 'base.html', {'message': 'Data profil belum terhubung.'})

    # LOGIC ADMIN (List + Filter + CRUD)
    alumni = Alumni.objects.select_related('prodi', 'fakultas').all()
    
    # Filter
    prodi_id = request.GET.get('prodi')
    tahun = request.GET.get('tahun')
    
    if prodi_id:
        alumni = alumni.filter(prodi_id=prodi_id)
    if tahun:
        alumni = alumni.filter(tahun_lulus=tahun)

    context = {
        'alumni_list': alumni,
        'prodi_list': Prodi.objects.all(), # Untuk filter
        'tahun_list': Alumni.objects.values_list('tahun_lulus', flat=True).distinct()
    }
    return render(request, 'alumni/alumni_list.html', context)

@login_required
@user_passes_test(is_admin)
def alumni_create(request):
    if request.method == 'POST':
        form = AlumniForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Alumni berhasil ditambahkan (User login dibuat otomatis).")
            return redirect('alumni:list')
    else:
        form = AlumniForm()
    
    # Pass fakultas list for JS filter
    fakultas_list = Fakultas.objects.all()
    return render(request, 'alumni/alumni_form.html', {'form': form, 'fakultas_list': fakultas_list})

@login_required
@user_passes_test(is_admin)
def alumni_edit(request, pk):
    alumni = get_object_or_404(Alumni, pk=pk)
    if request.method == 'POST':
        form = AlumniForm(request.POST, instance=alumni)
        if form.is_valid():
            form.save()
            messages.success(request, "Data alumni diperbarui.")
            return redirect('alumni:list')
    else:
        form = AlumniForm(instance=alumni)
    
    fakultas_list = Fakultas.objects.all()
    return render(request, 'alumni/alumni_form.html', {'form': form, 'fakultas_list': fakultas_list})

@login_required
@user_passes_test(is_admin)
def alumni_delete(request, pk):
    alumni = get_object_or_404(Alumni, pk=pk)
    if request.method == 'POST':
        # User associated will be kept or deleted? 
        # Usually user is deleted too if OneToOne, but Django default won't delete User unless specified.
        # Let's keep it simple: delete alumni data.
        user = alumni.user
        alumni.delete()
        if user:
            user.delete() # Cleanup user as well
        messages.success(request, "Alumni dihapus.")
        return redirect('alumni:list')
    return render(request, 'alumni/alumni_confirm_delete.html', {'object': alumni})

# AJAX endpoint for Prodi
def ajax_load_prodi(request):
    fakultas_id = request.GET.get('fakultas_id')
    prodi_list = Prodi.objects.filter(fakultas_id=fakultas_id).order_by('nama').values('id', 'nama')
    return JsonResponse(list(prodi_list), safe=False)