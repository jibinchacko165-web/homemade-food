from django import forms
from .models import FoodItem


class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ('name', 'description', 'price', 'category', 'image', 'is_available', 'preparation_time')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Food name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your dish'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price in ₹'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'preparation_time': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minutes'}),
        }
