from socket import fromshare
from django import forms
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    field_user_name = forms.CharField(max_length=255)
    user_address = forms.CharField(max_length=5000)
    user_contact = forms.CharField(max_length=20)
    user_email = forms.EmailField(max_length=255)
