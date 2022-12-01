from django import forms
from django.forms import DateField, DateInput, DateTimeInput, NumberInput, Textarea
from localflavor.br.forms import BRCPFField, BRCNPJField
from phonenumber_field.formfields import PhoneNumberField

from users.models import User

from .models import (Franquia, Loja, Meta, Produto,
                     Revendedor, Supervisor)


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field and isinstance(field , forms.TypedChoiceField):
                field.choices = field.choices[1:]

    class Meta:
        model = User
        fields = ['email', 'tipo']


class PerfilRevendedor(forms.ModelForm):

    cpf = BRCPFField()

    def __init__(self, *args, **kwargs):
        super(PerfilRevendedor, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field and isinstance(field , forms.TypedChoiceField):
                field.choices = field.choices[1:]
                
    class Meta:
        model = Revendedor
        exclude = ['user', 'supervisor']
        widgets = {
                'datanasc': DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'placeholder': 'Selecione uma data',
                    'type': 'date'
                }),
            }


class PerfilFranquia(forms.ModelForm):

    CNPJ = BRCNPJField()
                
    class Meta:
        model = Franquia
        exclude = ['user']


class PerfilLoja(forms.ModelForm):

    CNPJ = BRCNPJField()

    class Meta:
        model = Loja
        exclude = ['user', 'franquia', 'meta']


class PerfilSupervisor(forms.ModelForm):

    cpf = BRCPFField()

    def __init__(self, *args, **kwargs):
        super(PerfilSupervisor, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field and isinstance(field , forms.TypedChoiceField):
                field.choices = field.choices[1:]

    class Meta:
        model = Supervisor
        exclude = ['user', 'franquia']
        widgets = {
                'datanasc': DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'placeholder': 'Selecione uma data',
                    'type': 'date'
                }),
            }



class FormProduto(forms.ModelForm):
    class Meta:
        model = Produto
        fields = '__all__'


class formMeta(forms.ModelForm):
    class Meta:
        model = Meta
        exclude = ['nivel']
