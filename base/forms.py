from django import forms
from .models import Room


class RoomModelForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host','participants']