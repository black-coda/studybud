from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import ModelForm
from .models import Room
from django.contrib.auth.models import User

class RoomModelForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host','participants']


class UserModelForm(ModelForm):
    first_name = forms.CharField(max_length=300)
    class Meta:
        model = User
        fields = ['first_name','last_name', 'username', 'email']


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name', 'username', 'email', 'password1' ,'password2']