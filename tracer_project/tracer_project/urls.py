from django.contrib import admin
from django.urls import path, include
from tracer_project.custom_logout import LogoutAllowGetView
from .views import dashboard
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Dashboard
    path('', dashboard, name='dashboard'),

    # Auth
    path('login/', views.login_page, name='login'),
    path('logout/', LogoutAllowGetView.as_view(next_page='/login/'), name='logout'),

    # Apps
    path('alumni/', include('alumni.urls')),
    path('survey/', include('survey.urls')),
    path('statistik/', include('statistik.urls')),
    path('feedback/', include('feedback.urls')),
]
