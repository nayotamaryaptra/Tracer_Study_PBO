from django.db import models
from alumni.models import Alumni

class Survey(models.Model):
    STATUS_KERJA = [
        ('Bekerja', 'Bekerja'),
        ('Wirausaha', 'Wirausaha'),
        ('Belum Bekerja', 'Belum Bekerja'),
        ('Studi Lanjut', 'Studi Lanjut'),
    ]

    JENIS_PERUSAHAAN = [
        ('Swasta', 'Swasta'),
        ('Negeri', 'Negeri / BUMN'),
        ('StartUp', 'StartUp'),
        ('UMKM', 'UMKM'),
        ('Multinasional', 'Multinasional'),
    ]

    POSISI = [
        ('Staff', 'Staff'),
        ('Supervisor', 'Supervisor'),
        ('Manager', 'Manager'),
        ('Direktur', 'Direktur'),
        ('Lainnya', 'Lainnya'),
    ]

    KESESUAIAN = [
        ('Sangat Sesuai', 'Sangat Sesuai'),
        ('Sesuai', 'Sesuai'),
        ('Cukup', 'Cukup'),
        ('Kurang', 'Kurang'),
        ('Tidak Sesuai', 'Tidak Sesuai'),
    ]

    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE)
    status_pekerjaan = models.CharField(max_length=20, choices=STATUS_KERJA)
    waktu_tunggu = models.IntegerField(null=True, blank=True)
    jenis_perusahaan = models.CharField(max_length=20, choices=JENIS_PERUSAHAAN, null=True, blank=True)
    posisi_pekerjaan = models.CharField(max_length=20, choices=POSISI, null=True, blank=True)
    gaji = models.IntegerField(null=True, blank=True)
    kesesuaian_jurusan = models.CharField(max_length=20, choices=KESESUAIAN)
    catatan = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Survey: {self.alumni.nama} ({self.status_pekerjaan})"
