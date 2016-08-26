import django.contrib.auth.forms
from django.contrib.auth.models import User
from django import forms
from captcha.fields import ReCaptchaField
from django.forms.models import modelform_factory


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserCreationForm(django.contrib.auth.forms.UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'E-Mail'}), required=True)
    captcha = ReCaptchaField(use_ssl=False)
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    password2 = forms.CharField(label="Confirm Password",
                                widget=forms.PasswordInput(attrs={'placeholder': 'Verify Password'}))

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'User Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'E-Mail'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
        }
