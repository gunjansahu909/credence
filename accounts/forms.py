from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *

class DeveloperForm(ModelForm):
	class Meta:
		model = Developer
		fields = '__all__'
		exclude = ['user']

class ProjectForm(ModelForm):
	class Meta:
		model = Work_Status
		fields = '__all__'


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']