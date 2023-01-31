from django import forms
from django.contrib.auth.forms import UserCreationForm


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    second_name = forms.CharField(max_length=50)
    email = forms.EmailField()
