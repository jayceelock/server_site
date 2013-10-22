"""
This script creates a form that Django uses to save new users using an HTML template
"""

from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

class UserForm(ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = User
		fields = ('username', 'email', 'password')
