# alumni/urls.py
from django.urls import path
from . import views

app_name = 'alumni'

urlpatterns = [
    path('', views.alumni_list, name='list'),
    path('add/', views.alumni_create, name='create'),
    path('edit/<int:pk>/', views.alumni_edit, name='edit'),
    path('delete/<int:pk>/', views.alumni_delete, name='delete'),
    
    # URL AJAX (Baru)
    path('ajax/load-prodi/', views.ajax_load_prodi, name='ajax_load_prodi'),
]