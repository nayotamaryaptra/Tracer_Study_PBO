from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Feedback
from .forms import FeedbackForm
from alumni.models import Prodi, Alumni

@login_required
def feedback_list(request):
    # ADMIN: Bisa Update Status via POST
    if request.method == 'POST' and request.user.is_staff:
        feedback_id = request.POST.get('feedback_id')
        new_status = request.POST.get('status')
        if feedback_id and new_status:
            fb = get_object_or_404(Feedback, id=feedback_id)
            fb.status = new_status
            fb.save()
            messages.success(request, f"Status tiket #{fb.id} diperbarui.")
            return redirect('feedback:list')

    # ADMIN VIEW (Filter + All Data)
    if request.user.is_staff:
        feedbacks = Feedback.objects.select_related('alumni', 'alumni__prodi').all().order_by('-created_at')
        
        # Filter Logic
        kategori = request.GET.get('kategori')
        status = request.GET.get('status')
        
        if kategori: feedbacks = feedbacks.filter(kategori=kategori)
        if status: feedbacks = feedbacks.filter(status=status)
        
        context = {
            'feedbacks': feedbacks, 'is_admin': True,
            'kategori_list': Feedback.KATEGORI_CHOICES, # Untuk Filter Dropdown
            'status_list': Feedback.STATUS_CHOICES,
        }
        return render(request, 'feedback/feedback_list.html', context)
    
    # MAHASISWA VIEW (My Data Only)
    else:
        if not hasattr(request.user, 'alumni'): return redirect('dashboard')
        feedbacks = Feedback.objects.filter(alumni=request.user.alumni).order_by('-created_at')
        return render(request, 'feedback/feedback_list.html', {'feedbacks': feedbacks, 'is_admin': False})

@login_required
def feedback_create(request):
    if request.user.is_staff:
        return redirect('feedback:list')
    if not hasattr(request.user, 'alumni'):
        return redirect('dashboard')

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            fb = form.save(commit=False)
            fb.alumni = request.user.alumni
            fb.save()
            messages.success(request, "Aspirasi Anda berhasil dikirim!")
            return redirect('feedback:list')
    else:
        form = FeedbackForm()
    
    return render(request, 'feedback/feedback_form.html', {'form': form, 'title': 'Kirim Aspirasi Baru'})

@login_required
def feedback_edit(request, pk):
    fb = get_object_or_404(Feedback, pk=pk)
    if request.user.is_staff or fb.alumni.user != request.user:
        return redirect('feedback:list')

    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=fb)
        if form.is_valid():
            form.save()
            messages.success(request, "Aspirasi diperbarui.")
            return redirect('feedback:list')
    else:
        form = FeedbackForm(instance=fb)
    return render(request, 'feedback/feedback_form.html', {'form': form, 'title': 'Edit Aspirasi'})

@login_required
def feedback_delete(request, pk):
    fb = get_object_or_404(Feedback, pk=pk)
    is_owner = (not request.user.is_staff and fb.alumni.user == request.user)
    if not (request.user.is_staff or is_owner):
        return redirect('feedback:list')

    if request.method == 'POST':
        fb.delete()
        messages.success(request, "Data dihapus.")
        return redirect('feedback:list')
    return render(request, 'feedback/feedback_confirm_delete.html', {'object': fb})