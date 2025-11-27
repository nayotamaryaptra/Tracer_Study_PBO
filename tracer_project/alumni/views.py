from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Alumni
from .forms import AlumniForm

# LIST
@login_required
def alumni_list(request):
    data = Alumni.objects.all()
    return render(request, 'alumni/alumni_list.html', {"alumni_list": data})

# CREATE
@login_required
def alumni_create(request):
    form = AlumniForm()
    if request.method == "POST":
        form = AlumniForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('alumni_list')
    return render(request, 'alumni/alumni_form.html', {"form": form, "title": "Tambah Alumni"})

# EDIT
@login_required
def alumni_edit(request, pk):
    alumni = get_object_or_404(Alumni, pk=pk)
    form = AlumniForm(instance=alumni)
    if request.method == "POST":
        form = AlumniForm(request.POST, instance=alumni)
        if form.is_valid():
            form.save()
            return redirect('alumni_list')
    return render(request, 'alumni/alumni_form.html', {"form": form, "title": "Edit Alumni"})

# DELETE
@login_required
def alumni_delete(request, pk):
    alumni = get_object_or_404(Alumni, pk=pk)
    if request.method == "POST":
        alumni.delete()
        return redirect('alumni_list')
    return render(request, 'alumni/alumni_delete.html', {"alumni": alumni})

# DETAIL
@login_required
def alumni_detail(request, pk):
    alumni = get_object_or_404(Alumni, pk=pk)
    return render(request, 'alumni/alumni_detail.html', {"alumni": alumni})
