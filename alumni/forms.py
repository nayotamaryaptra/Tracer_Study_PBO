from django import forms
from .models import Alumni, Prodi, Fakultas

class AlumniForm(forms.ModelForm):
    # Tambahkan field Fakultas secara eksplisit agar muncul di form
    fakultas = forms.ModelChoiceField(
        queryset=Fakultas.objects.all(),
        label="Pilih Fakultas",
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Alumni
        # Urutan: Pilih Fakultas dulu -> Baru Prodi
        fields = ['nim', 'nama', 'email', 'tahun_lulus', 'fakultas', 'prodi']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Default: Kosongkan Prodi dulu sebelum Fakultas dipilih
        self.fields['prodi'].queryset = Prodi.objects.none()

        # LOGIKA 1: Jika ada data POST (User baru klik submit tapi error, atau sedang milih)
        if 'fakultas' in self.data:
            try:
                fakultas_id = int(self.data.get('fakultas'))
                self.fields['prodi'].queryset = Prodi.objects.filter(fakultas_id=fakultas_id).order_by('nama')
            except (ValueError, TypeError):
                pass  # Input tidak valid
        
        # LOGIKA 2: Jika sedang EDIT data (Form sudah terisi)
        elif self.instance.pk and self.instance.prodi:
            # Set initial Fakultas sesuai Prodi yang tersimpan
            self.fields['fakultas'].initial = self.instance.prodi.fakultas
            # Isi dropdown prodi sesuai fakultas tersebut
            self.fields['prodi'].queryset = self.instance.prodi.fakultas.prodi.order_by('nama')