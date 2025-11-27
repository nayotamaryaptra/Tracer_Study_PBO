from django.db import models

class Alumni(models.Model):
    STATUS_CHOICES = [
        ('Bekerja', 'Bekerja'),
        ('Belum Bekerja', 'Belum Bekerja'),
        ('Wirausaha', 'Wirausaha'),
        ('Studi Lanjut', 'Studi Lanjut'),
    ]

    nim = models.CharField(max_length=20, unique=True)
    nama = models.CharField(max_length=100)
    prodi = models.CharField(max_length=100)
    tahun_lulus = models.IntegerField()
    email = models.EmailField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Belum Bekerja")

    def __str__(self):
        return f"{self.nim} - {self.nama}"
