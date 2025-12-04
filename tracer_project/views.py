# tracer_project/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Simple placeholder dashboard
def dashboard(request):
    return render(request, 'dashboard.html')