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

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = models.User
        fields = ['email']

class PerfilRevendedor(forms.ModelForm):
    
    # def __init__(self, user, *args, **kwargs):
    #     self.user = user
    #     super(PerfilRevendedor, self).__init__(*args, **kwargs)
    
    class Meta:
        model = models.Revendedor
        fields =['nome','cpf','telefone','endereco','datanasc']