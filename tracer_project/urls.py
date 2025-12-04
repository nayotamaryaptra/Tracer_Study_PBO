# tracer_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    
    # Auth Views
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Apps URLs
    path('alumni/', include('alumni.urls')),
    path('survey/', include('survey.urls')), # Uncomment later
    path('feedback/', include('feedback.urls')), # Uncomment later
    path('statistik/', include('statistik.urls')), # Uncomment later
]