from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import password_validation
from django.forms import CharField, DateField
from phonenumber_field.formfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _

from . import models


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = models.User
        fields = ['email', ]
