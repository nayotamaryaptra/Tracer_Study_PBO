from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    # Sesuaikan dengan field baru di models.py
    list_display = ('alumni', 'mata_kuliah', 'kategori', 'rating', 'status', 'created_at')
    
    # Filter juga harus disesuaikan
    list_filter = ('kategori', 'status', 'rating', 'created_at', 'alumni__prodi')
    
    search_fields = ('mata_kuliah', 'saran', 'alumni__nama')
    
    # Supaya admin bisa ubah status langsung di list (opsional)
    list_editable = ('status',)