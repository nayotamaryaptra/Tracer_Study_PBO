from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Feedback
from .forms import FeedbackForm

@login_required
def feedback_list(request):
    data = Feedback.objects.select_related("alumni").all()
    return render(request, "feedback/feedback_list.html", {"feedback_list": data})

@login_required
def feedback_create(request):
    form = FeedbackForm()
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("feedback_list")
    return render(request, "feedback/feedback_form.html", {"form": form, "title": "Tambah Feedback"})

@login_required
def feedback_edit(request, pk):
    fb = get_object_or_404(Feedback, pk=pk)
    form = FeedbackForm(instance=fb)
    if request.method == "POST":
        form = FeedbackForm(request.POST, instance=fb)
        if form.is_valid():
            form.save()
            return redirect("feedback_list")
    return render(request, "feedback/feedback_form.html", {"form": form, "title": "Edit Feedback"})

@login_required
def feedback_delete(request, pk):
    fb = get_object_or_404(Feedback, pk=pk)
    if request.method == "POST":
        fb.delete()
        return redirect("feedback_list")
    return render(request, "feedback/feedback_delete.html", {"feedback": fb})

@login_required
def feedback_detail(request, pk):
    fb = get_object_or_404(Feedback, pk=pk)
    return render(request, "feedback/feedback_detail.html", {"feedback": fb})
