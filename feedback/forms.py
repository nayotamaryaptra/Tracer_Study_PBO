from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['mata_kuliah', 'kesesuaian', 'saran']
        widgets = {
            'saran': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tuliskan saran untuk kurikulum...'}),
        }