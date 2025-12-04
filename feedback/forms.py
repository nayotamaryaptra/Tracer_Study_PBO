from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['kategori', 'mata_kuliah', 'rating', 'saran', 'is_anonymous']
        widgets = {
            'rating': forms.RadioSelect(choices=[
                (5, '⭐⭐⭐⭐⭐ (Sangat Puas)'),
                (4, '⭐⭐⭐⭐ (Puas)'),
                (3, '⭐⭐⭐ (Cukup)'),
                (2, '⭐⭐ (Kurang)'),
                (1, '⭐ (Sangat Kurang)'),
            ]),
            'saran': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Jelaskan detail masukan Anda...'}),
            'mata_kuliah': forms.TextInput(attrs={'placeholder': 'Contoh: Pemrograman Web / AC Ruang B201'}),
        }