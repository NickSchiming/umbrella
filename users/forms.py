from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from . import models
from vendas import models


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = models.User
        fields = ['email',]
