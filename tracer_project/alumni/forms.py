from django import forms
from .models import Alumni

class AlumniForm(forms.ModelForm):
    class Meta:
        model = Alumni
        fields = ['nim', 'nama', 'prodi', 'tahun_lulus', 'email', 'status']

        widgets = {
            'nim': forms.TextInput(attrs={'class': 'form-control'}),
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'prodi': forms.TextInput(attrs={'class': 'form-control'}),
            'tahun_lulus': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
