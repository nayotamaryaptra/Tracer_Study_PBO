from django.urls import path
from . import views

urlpatterns = [
    path('', views.feedback_list, name='feedback_list'),
    path('create/', views.feedback_create, name='feedback_create'),
    path('edit/<int:pk>/', views.feedback_edit, name='feedback_edit'),
    path('delete/<int:pk>/', views.feedback_delete, name='feedback_delete'),
    path('detail/<int:pk>/', views.feedback_detail, name='feedback_detail'),
]
