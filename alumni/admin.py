# alumni/admin.py
from django.contrib import admin
from .models import Fakultas, Prodi, Alumni

@admin.register(Fakultas)
class FakultasAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama')

@admin.register(Prodi)
class ProdiAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama', 'fakultas')
    list_filter = ('fakultas',)

@admin.register(Alumni)
class AlumniAdmin(admin.ModelAdmin):
    # Hapus 'gaji_terakhir' dari list_display jika ada
    list_display = ('nim', 'nama', 'email', 'prodi', 'tahun_lulus', 'status_bekerja')
    search_fields = ('nim', 'nama', 'email')
    list_filter = ('prodi__fakultas', 'prodi', 'tahun_lulus', 'status_bekerja')
    
    # Hapus 'gaji_terakhir' dari readonly_fields
    readonly_fields = ('fakultas', 'user', 'status_bekerja')