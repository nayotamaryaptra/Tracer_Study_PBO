# alumni/models.py
from django.db import models
from django.contrib.auth.models import User

class Fakultas(models.Model):
    nama = models.CharField(max_length=100)

    def __str__(self):
        return self.nama
    
    class Meta:
        verbose_name_plural = "Fakultas"

class Prodi(models.Model):
    fakultas = models.ForeignKey(Fakultas, on_delete=models.CASCADE, related_name='prodi')
    nama = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nama} ({self.fakultas.nama})"
    
    class Meta:
        verbose_name_plural = "Prodi"

class Alumni(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='alumni', null=True, blank=True)
    
    nim = models.CharField(max_length=20, unique=True)
    nama = models.CharField(max_length=200)
    email = models.EmailField(unique=True) # Tambahan field Email (Wajib & Unik)
    tahun_lulus = models.IntegerField()
    
    prodi = models.ForeignKey('Prodi', on_delete=models.SET_NULL, null=True, related_name='alumni')
    fakultas = models.ForeignKey('Fakultas', on_delete=models.SET_NULL, null=True, blank=True, related_name='alumni')
    
    status_bekerja = models.BooleanField(default=False) 
    # Gaji kita hapus dari sini karena hitungannya dinamis dari Survey, 
    # atau biarkan null=True jika hanya untuk cache.

    def save(self, *args, **kwargs):
        if self.prodi:
            self.fakultas = self.prodi.fakultas
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nim} - {self.nama}"

    class Meta:
        verbose_name_plural = "Alumni"