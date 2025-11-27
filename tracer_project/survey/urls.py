from django.urls import path
from . import views

urlpatterns = [
    path('', views.survey_list, name='survey_list'),
    path('create/', views.survey_create, name='survey_create'),
    path('edit/<int:pk>/', views.survey_edit, name='survey_edit'),
    path('delete/<int:pk>/', views.survey_delete, name='survey_delete'),
]
