from django.urls import path
from . import views

urlpatterns = [
    path('', views.statistik_index, name='statistik_index'),
]
