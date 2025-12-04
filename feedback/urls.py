from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('', views.feedback_list, name='list'),
    path('add/', views.feedback_create, name='create'),
    path('edit/<int:pk>/', views.feedback_edit, name='edit'),
    path('delete/<int:pk>/', views.feedback_delete, name='delete'),
]