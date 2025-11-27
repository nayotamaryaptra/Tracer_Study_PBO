from django.urls import path
from . import views

urlpatterns = [
    path('', views.alumni_list, name='alumni_list'),
    path('create/', views.alumni_create, name='alumni_create'),
    path('edit/<int:pk>/', views.alumni_edit, name='alumni_edit'),
    path('delete/<int:pk>/', views.alumni_delete, name='alumni_delete'),
    path('detail/<int:pk>/', views.alumni_detail, name='alumni_detail'),
]
