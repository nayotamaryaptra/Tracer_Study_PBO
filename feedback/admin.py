from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('alumni', 'mata_kuliah', 'kesesuaian', 'created_at')
    # Filter by Mata Kuliah, dan Prodi/Tahun Lulus (via Relasi Alumni)
    list_filter = ('mata_kuliah', 'kesesuaian', 'alumni__prodi', 'alumni__tahun_lulus')
    search_fields = ('mata_kuliah', 'alumni__nama', 'saran')