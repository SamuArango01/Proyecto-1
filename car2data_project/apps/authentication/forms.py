from django import forms
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-turquoise'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-turquoise'}),
            'email': forms.EmailInput(attrs={'class': 'w-full border border-gray-300 rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-turquoise'}),
        }
