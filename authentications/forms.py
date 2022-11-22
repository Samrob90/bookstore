from django import forms
from authentications.models import Account
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control rounded-0 height-4 px-4",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control rounded-0 height-4 px-4",
            }
        )
    )


class RegisterForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ("first_name", "last_name", "email", "password1", "password2")
