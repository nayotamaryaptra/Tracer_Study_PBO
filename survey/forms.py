from django import forms
from .models import Survey

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['perusahaan', 'tahun_masuk', 'bidang_pekerjaan', 'kesesuaian', 'gaji']
        widgets = {
            'tahun_masuk': forms.NumberInput(attrs={'placeholder': 'Contoh: 2023'}),
        }