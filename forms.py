from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Event


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class EventCreationForm(forms.Form):
    Name = forms.CharField(max_length=250)
    Location = forms.CharField(max_length=250)
    #Time = forms.DateTimeField()
    #Time = forms.DateTimeField(input_formats=["%d %b %Y %H:%M:%S %Z"])







