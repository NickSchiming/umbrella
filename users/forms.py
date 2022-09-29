from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import password_validation
from django.forms import CharField, DateField
from phonenumber_field.formfields import PhoneNumberField

from . import models


class UserRegisterForm(UserCreationForm):
    username = UsernameField(
        label='E-mail',
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    nome = forms.CharField(label='Nome completo:', max_length=100)
    cpf = forms.CharField(max_length=100)
    telefone = PhoneNumberField()
    endereco = CharField(max_length=150)
    datanasc = DateField()
    password1 = forms.CharField(
        label="Senha:",
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )

    class Meta:
        model = models.Usuario
        fields = ['username', 'nome', 'cpf', 'telefone', 'endereco',
                  'datanasc', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['telefone'].widget.attrs.update({'class': 'mask-telefone'})
        self.fields['datanasc'].widget.attrs.update({'class': 'mask-datanasc'})
        self.fields['cpf'].widget.attrs.update({'class': 'mask-cpf'})
