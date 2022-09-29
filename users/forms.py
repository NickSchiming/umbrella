from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label="E-mail:")
    nome = forms.CharField(label='Nome completo:', max_length=100)
    password1 = forms.CharField(
        label="Senha:",
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )

    class Meta:
        model = User
        fields = ['nome', 'email', 'password1', 'password2']
