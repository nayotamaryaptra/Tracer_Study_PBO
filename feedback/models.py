from django.db import models
from alumni.models import Alumni

class Feedback(models.Model):
    # Pilihan Sesuai Spec: B (Sangat sesuai) — Sesuai — Kurang — Tidak sesuai
    KESESUAIAN_CHOICES = [
        ('Sangat Sesuai', 'Sangat Sesuai'),
        ('Sesuai', 'Sesuai'),
        ('Kurang', 'Kurang'),
        ('Tidak Sesuai', 'Tidak Sesuai'),
    ]

    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE, related_name='feedbacks')
    mata_kuliah = models.CharField(max_length=200, verbose_name="Nama Mata Kuliah")
    kesesuaian = models.CharField(max_length=20, choices=KESESUAIAN_CHOICES)
    saran = models.TextField(verbose_name="Saran Perbaikan")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mata_kuliah} - {self.alumni.nama}"