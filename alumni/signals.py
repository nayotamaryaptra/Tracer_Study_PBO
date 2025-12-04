# alumni/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Alumni

@receiver(post_save, sender=Alumni)
def create_user_for_alumni(sender, instance, created, **kwargs):
    if created and not instance.user:
        # LOGIKA BARU SESUAI GAMBAR:
        # Username = Email
        # Password = NIM
        
        username = instance.email.lower().strip()
        password = instance.nim.strip()
        
        # Buat user baru
        user = User.objects.create_user(
            username=username, # Email dijadikan username login
            email=instance.email,
            password=password,
            first_name=instance.nama
        )
        instance.user = user
        instance.save()
        print(f"DEBUG: User created. Login: {username} | Pass: {password}")