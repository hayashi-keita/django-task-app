from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'full_name', 'email', 'department')
        labels = {
            'full_name': 'フルネーム',
            'department': '部署',
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'full_name', 'email', 'department')
        labels = {
            'full_name': 'フルネーム',
            'department': '部署',
        }