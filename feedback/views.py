from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Feedback
from .forms import FeedbackForm
from alumni.models import Prodi, Alumni
from django import forms

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['mata_kuliah', 'kesesuaian', 'saran']

def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
def feedback_list(request):
    # ADMIN: Lihat Semua + Filter (Matkul, Prodi, Tahun) - NO Jurusan
    if request.user.is_staff:
        feedbacks = Feedback.objects.select_related('alumni', 'alumni__prodi').all()
        
        # Filter
        matkul = request.GET.get('matkul')
        prodi_id = request.GET.get('prodi')
        tahun = request.GET.get('tahun')
        
        if matkul: feedbacks = feedbacks.filter(mata_kuliah__icontains=matkul)
        if prodi_id: feedbacks = feedbacks.filter(alumni__prodi_id=prodi_id)
        if tahun: feedbacks = feedbacks.filter(alumni__tahun_lulus=tahun)
        
        context = {
            'feedbacks': feedbacks, 'is_admin': True,
            'prodi_list': Prodi.objects.all(),
            'tahun_list': Alumni.objects.values_list('tahun_lulus', flat=True).distinct()
        }
        return render(request, 'feedback/feedback_list.html', context)
    
    # MAHASISWA: Lihat Punya Sendiri
    else:
        if not hasattr(request.user, 'alumni'): return redirect('dashboard')
        feedbacks = Feedback.objects.filter(alumni=request.user.alumni)
        return render(request, 'feedback/feedback_list.html', {'feedbacks': feedbacks, 'is_admin': False})

@login_required
def feedback_create(request):
    # SECURITY: Admin DILARANG Tambah Feedback
    if request.user.is_staff:
        messages.error(request, "Admin tidak dapat mengisi feedback.")
        return redirect('feedback:list')

    # Cek apakah user punya profil alumni
    if not hasattr(request.user, 'alumni'):
        messages.error(request, "Profil alumni tidak ditemukan.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            fb = form.save(commit=False)
            fb.alumni = request.user.alumni # Otomatis set Alumni
            fb.save()
            messages.success(request, "Feedback berhasil dikirim.")
            return redirect('feedback:list')
    else:
        form = FeedbackForm()
    
    return render(request, 'feedback/feedback_form.html', {'form': form, 'title': 'Tambah Feedback'})

@login_required
def feedback_edit(request, pk):
    fb = get_object_or_404(Feedback, pk=pk)

    # SECURITY: Hanya Pemilik yang boleh edit
    if request.user.is_staff or fb.alumni.user != request.user:
        messages.error(request, "Akses ditolak.")
        return redirect('feedback:list')

    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=fb)
        if form.is_valid():
            form.save()
            messages.success(request, "Feedback diperbarui.")
            return redirect('feedback:list')
    else:
        form = FeedbackForm(instance=fb)

    return render(request, 'feedback/feedback_form.html', {'form': form, 'title': 'Edit Feedback'})

@login_required
def feedback_delete(request, pk):
    fb = get_object_or_404(Feedback, pk=pk)
    
    # SECURITY: Admin BOLEH, Pemilik BOLEH
    is_owner = (not request.user.is_staff and fb.alumni.user == request.user)
    if not (request.user.is_staff or is_owner):
        return redirect('feedback:list')

    if request.method == 'POST':
        fb.delete()
        messages.success(request, "Feedback dihapus.")
        return redirect('feedback:list')
    
    return render(request, 'feedback/feedback_confirm_delete.html', {'object': fb})