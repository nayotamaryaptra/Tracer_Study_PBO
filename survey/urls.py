from django.urls import path
from . import views

app_name = 'survey'

urlpatterns = [
    path('', views.survey_list, name='list'),
    path('add/', views.survey_create, name='create'),
    path('edit/<int:pk>/', views.survey_edit, name='edit'),
    path('delete/<int:pk>/', views.survey_delete, name='delete'),
]