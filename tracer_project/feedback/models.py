from django.db import models
from alumni.models import Alumni

RATING = [
    (1, '1 - Sangat Buruk'),
    (2, '2 - Buruk'),
    (3, '3 - Cukup'),
    (4, '4 - Baik'),
    (5, '5 - Sangat Baik'),
]

class Feedback(models.Model):
    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE)
    rating_kurikulum = models.IntegerField(choices=RATING)
    rating_pengajar = models.IntegerField(choices=RATING)
    rating_relevansi = models.IntegerField(choices=RATING)

    komentar = models.TextField()
    saran = models.TextField(blank=True, null=True)

    tanggal_input = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback dari {self.alumni.nama}"
