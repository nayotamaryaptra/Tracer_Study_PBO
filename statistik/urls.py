from django.urls import path
from . import views

app_name = 'statistik'

urlpatterns = [
    path('', views.statistik_dashboard, name='dashboard'),
    path('export-pdf/', views.export_pdf, name='export_pdf'),
]