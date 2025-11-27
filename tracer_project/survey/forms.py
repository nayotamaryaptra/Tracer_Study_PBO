from django import forms
from .models import Survey

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = [
            'alumni',
            'status_pekerjaan',
            'waktu_tunggu',
            'jenis_perusahaan',
            'posisi_pekerjaan',
            'gaji',
            'kesesuaian_jurusan',
            'catatan',
        ]

        widgets = {
            'alumni': forms.Select(attrs={'class': 'form-select'}),
            'status_pekerjaan': forms.Select(attrs={'class': 'form-select'}),
            'waktu_tunggu': forms.NumberInput(attrs={'class': 'form-control'}),
            'jenis_perusahaan': forms.Select(attrs={'class': 'form-select'}),
            'posisi_pekerjaan': forms.Select(attrs={'class': 'form-select'}),
            'gaji': forms.NumberInput(attrs={'class': 'form-control'}),
            'kesesuaian_jurusan': forms.Select(attrs={'class': 'form-select'}),
            'catatan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
