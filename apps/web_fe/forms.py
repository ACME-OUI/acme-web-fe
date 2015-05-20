from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from captcha.fields import ReCaptchaField
from django.forms.models import modelform_factory


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    # captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    captcha = ReCaptchaField(attrs={'theme': 'blackglass'})

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
