from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegister(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
