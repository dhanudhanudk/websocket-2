# myapp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.exceptions import ValidationError
from django.contrib import messages

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    class Meta:
        model = User
        fields = ("name", "email", "phonenumber", "password")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.data["password"])  # Hash the password
        if commit:
            user.save()
        return user
    
class LoginForm(forms.Form):
    email=forms.EmailField(label="email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    class Meta:
        model = User
        fields = ("email", "password")
