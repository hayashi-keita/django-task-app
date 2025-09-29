from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'full_name', 'email', 'department', 'image')
        labels = {
            'full_name': 'フルネーム',
            'department': '部署',
            'image': '画像',
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'full_name', 'email', 'department', 'image')
        labels = {
            'full_name': 'フルネーム',
            'department': '部署',
            'image': '画像',
        }