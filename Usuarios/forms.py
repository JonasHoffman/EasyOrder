from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):

    username = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(
            attrs={
                "class": "login-input",
                "placeholder": "Digite seu e-mail",
                "autocomplete": "email",
            }
        )
    )

    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(
            attrs={
                "class": "login-input",
                "placeholder": "Digite sua senha",
                "autocomplete": "current-password",
            }
        )
    )