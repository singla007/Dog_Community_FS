from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from dog_community_app.models import Dogs


# class DogCreationForm(forms.ModelForm):
# 	class Meta:
# 		model = Dogs
# 		fields = ['is_adopted','dog_name', 'dog_color', 'dog_age', 'is_disable', 'disabilty', 'unique_identification', 'is_adoption_ready', 'dog_image']

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2'] 