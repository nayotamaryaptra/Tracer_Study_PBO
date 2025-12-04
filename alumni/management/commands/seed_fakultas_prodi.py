from django.core.management.base import BaseCommand
from alumni.models import Fakultas, Prodi

class Command(BaseCommand):
    help = 'Seeds Fakultas and Prodi data based on Real UNNES Data'

    def handle(self, *args, **kwargs):
        # Data Lengkap sesuai request user
        data_kampus = {
            "Fakultas Ilmu Pendidikan dan Psikologi": [
                "Bimbingan dan Konseling",
                "Teknologi Pendidikan",
                "Pendidikan Non Formal",
                "Psikologi",
                "Pendidikan Guru Sekolah Dasar",
                "Pendidikan Guru PAUD"
            ],
            "Fakultas Matematika & Ilmu Pengetahuan Alam": [
                "Statistika Terapan dan Komputasi", # Diploma
                "Pendidikan Matematika",
                "Matematika",
                "Pendidikan Fisika",
                "Fisika",
                "Pendidikan Kimia",
                "Kimia",
                "Pendidikan Biologi",
                "Biologi",
                "Pendidikan Ilmu Pengetahuan Alam",
                "Teknik Informatika",
                "Sistem Informasi",
                "Ilmu Lingkungan",
                "Statistika dan Sains Data"
            ],
            "Fakultas Ekonomika dan Bisnis": [
                "Manajemen",
                "Akuntansi",
                "Ekonomi Pembangunan",
                "Pendidikan Ekonomi",
                "Pendidikan Akuntansi",
                "Pendidikan Administrasi Perkantoran",
                "Ekonomi & Keuangan Islam"
            ],
            "Fakultas Bahasa dan Seni": [
                "Desain Komunikasi Visual", # Diploma
                "Pendidikan Bahasa dan Sastra Indonesia",
                "Sastra Indonesia",
                "Pendidikan Bahasa Inggris",
                "Sastra Inggris",
                "Pendidikan Bahasa Perancis",
                "Sastra Perancis",
                "Pendidikan Bahasa Jepang",
                "Pendidikan Bahasa Arab",
                "Pendidikan Bahasa Mandarin",
                "Pendidikan Seni Rupa",
                "Seni Rupa",
                "Pendidikan Seni Musik",
                "Pendidikan Seni Tari",
                "Pendidikan Bahasa Jawa",
                "Sastra Jawa"
            ],
            "Fakultas Hukum": [
                "Ilmu Hukum"
            ],
            "Fakultas Teknik": [
                "Pendidikan Teknik Bangunan",
                "Teknik Sipil",
                "Arsitektur",
                "Pendidikan Teknik Mesin",
                "Teknik Mesin",
                "Pendidikan Teknik Otomotif",
                "Pendidikan Teknik Elektro",
                "Teknik Elektro",
                "Pendidikan Teknik Informatika dan Komputer",
                "Pendidikan Kesejahteraan Keluarga",
                "Pendidikan Tata Kecantikan",
                "Pendidikan Tata Boga",
                "Pendidikan Tata Busana",
                "Teknik Kimia",
                "Teknik Komputer"
            ],
            "Fakultas Kedokteran": [
                "Kedokteran",
                "Kedokteran Hewan",
                "Ilmu Kesehatan Masyarakat",
                "Gizi",
                "Farmasi"
            ],
            "Fakultas Ilmu Sosial dan Ilmu Politik": [
                "Pendidikan Sosiologi dan Antropologi",
                "Pendidikan Pancasila dan Kewarganegaraan",
                "Pendidikan Sejarah",
                "Ilmu Sejarah",
                "Ilmu Politik",
                "Geografi",
                "Pendidikan Geografi",
                "Pendidikan Ilmu Pengetahuan Sosial",
                "Ilmu Komunikasi"
            ],
            "Fakultas Ilmu Keolahragaan": [
                "Ilmu Keolahragaan",
                "Pendidikan Kesehatan Jasmani dan Rekreasi",
                "Pendidikan Jasmani Sekolah Dasar",
                "Pendidikan Kepelatihan Olahraga"
            ]
        }

        self.stdout.write("Mulai mengisi data Fakultas & Prodi...")

        for nama_fakultas, list_prodi in data_kampus.items():
            # Create Fakultas
            fakultas, created = Fakultas.objects.get_or_create(nama=nama_fakultas)
            if created:
                self.stdout.write(self.style.SUCCESS(f"[+] Fakultas dibuat: {nama_fakultas}"))
            else:
                self.stdout.write(self.style.WARNING(f"[*] Fakultas sudah ada: {nama_fakultas}"))
            
            # Create Prodi
            for nama_prodi in list_prodi:
                prodi, p_created = Prodi.objects.get_or_create(fakultas=fakultas, nama=nama_prodi)
                if p_created:
                    self.stdout.write(f"   - Prodi dibuat: {nama_prodi}")
        
        self.stdout.write(self.style.SUCCESS('SELESAI! Semua data Fakultas & Prodi berhasil di-seed.'))