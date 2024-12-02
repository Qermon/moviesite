from django import forms
from .models import Rating, UserProfile


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['review', 'user_rate']
        widgets = {
            'review': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your review',
                'rows': 4
            }),
            'user_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_rate'].initial = 0


class AvatarForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']
