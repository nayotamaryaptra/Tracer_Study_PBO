from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Survey
from .forms import SurveyForm

@login_required
def survey_list(request):
    data = Survey.objects.select_related("alumni").all()
    return render(request, 'survey/survey_list.html', {"survey_list": data})

@login_required
def survey_create(request):
    form = SurveyForm()
    if request.method == "POST":
        form = SurveyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('survey_list')
    return render(request, 'survey/survey_form.html', {"form": form, "title": "Tambah Survey"})

@login_required
def survey_edit(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    form = SurveyForm(instance=survey)
    if request.method == "POST":
        form = SurveyForm(request.POST, instance=survey)
        if form.is_valid():
            form.save()
            return redirect('survey_list')
    return render(request, 'survey/survey_form.html', {"form": form, "title": "Edit Survey"})

@login_required
def survey_delete(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    if request.method == "POST":
        survey.delete()
        return redirect('survey_list')
    return render(request, 'survey/survey_delete.html', {"survey": survey})
