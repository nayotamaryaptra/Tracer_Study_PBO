from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from alumni.models import Alumni

class Survey(models.Model):
    KESESUAIAN_CHOICES = [
        ('Sangat Sesuai', 'Sangat Sesuai'),
        ('Sesuai', 'Sesuai'),
        ('Kurang', 'Kurang'),
        ('Tidak Sesuai', 'Tidak Sesuai'),
    ]

    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE, related_name='surveys')
    perusahaan = models.CharField(max_length=200)
    tahun_masuk = models.IntegerField()
    bidang_pekerjaan = models.CharField(max_length=200) # Free text
    kesesuaian = models.CharField(max_length=20, choices=KESESUAIAN_CHOICES)
    gaji = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.perusahaan} - {self.alumni.nama}"

# Business Rule: Update Status Bekerja Alumni
@receiver(post_save, sender=Survey)
@receiver(post_delete, sender=Survey)
def update_status_bekerja(sender, instance, **kwargs):
    alumni = instance.alumni
    # Jika punya minimal 1 survey, dianggap bekerja
    count = alumni.surveys.count()
    alumni.status_bekerja = count > 0
    alumni.save()