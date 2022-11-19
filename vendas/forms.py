from django import forms

from users.models import User

from .models import (Franquia, Loja, Meta, Produto,
                     Revendedor, Supervisor)


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'tipo']


class PerfilRevendedor(forms.ModelForm):
    class Meta:
        model = Revendedor
        exclude = ['user', 'supervisor']


class PerfilFranquia(forms.ModelForm):
    class Meta:
        model = Franquia
        exclude = ['user']


class PerfilLoja(forms.ModelForm):
    class Meta:
        model = Loja
        exclude = ['user', 'franquia', 'meta']


class PerfilSupervisor(forms.ModelForm):
    class Meta:
        model = Supervisor
        exclude = ['user', 'franquia']


class FormProduto(forms.ModelForm):
    class Meta:
        model = Produto
        fields = '__all__'


class formMeta(forms.ModelForm):
    class Meta:
        model = Meta
        exclude = ['nivel']
