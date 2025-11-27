from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = [
            'alumni',
            'rating_kurikulum',
            'rating_pengajar',
            'rating_relevansi',
            'komentar',
            'saran',
        ]

        widgets = {
            'alumni': forms.Select(attrs={'class': 'form-select'}),
            'rating_kurikulum': forms.Select(attrs={'class': 'form-select'}),
            'rating_pengajar': forms.Select(attrs={'class': 'form-select'}),
            'rating_relevansi': forms.Select(attrs={'class': 'form-select'}),
            'komentar': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'saran': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
