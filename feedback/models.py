from django.db import models
from alumni.models import Alumni

class Feedback(models.Model):
    # 2. Kategori Masukan
    KATEGORI_CHOICES = [
        ('Akademik', 'Akademik & Kurikulum'),
        ('Fasilitas', 'Fasilitas & Sarana'),
        ('Pelayanan', 'Pelayanan Dosen/Staff'),
        ('Lainnya', 'Lainnya'),
    ]

    # 3. Status Tiket (Tracking)
    STATUS_CHOICES = [
        ('pending', 'Menunggu Review'),
        ('process', 'Sedang Diproses'),
        ('done', 'Selesai / Ditindaklanjuti'),
    ]

    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE, related_name='feedbacks')
    
    # Field Utama
    mata_kuliah = models.CharField(max_length=200, verbose_name="Subjek / Mata Kuliah")
    kategori = models.CharField(max_length=20, choices=KATEGORI_CHOICES, default='Akademik')
    
    # 1. Rating Bintang (1-5)
    rating = models.IntegerField(default=5, verbose_name="Rating Kepuasan")
    
    saran = models.TextField(verbose_name="Detail Masukan")
    
    # 3. Status (Default: Pending)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # 5. Mode Anonim
    is_anonymous = models.BooleanField(default=False, verbose_name="Kirim sebagai Anonim")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mata_kuliah} - {self.kategori}"