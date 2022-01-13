from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Room,Profile
from django.contrib.auth.models import User

class RoomModelForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host','participants']


class UserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name', 'username', 'email',]


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name', 'username', 'email', 'password1' ,'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']