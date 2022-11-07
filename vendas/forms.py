from django import forms
from .models import Franquia, Loja, Meta, Produto, Produto, Revendedor, Pedido, ItemPedido, Supervisor
from users.models import User


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'type']


class PerfilRevendedor(forms.ModelForm):
    class Meta:
        model = Revendedor
        fields = ['nome', 'cpf', 'telefone','cep',
                  'endereco', 'datanasc', 'is_aprovado']

class PerfilFranquia(forms.ModelForm):
    class Meta:
        model = Franquia
        fields = ['razaosocial','cnpj','endereco']

class PerfilLoja(forms.ModelForm):
    class Meta:
        model = Loja
        fields = ['razaosocial','cnpj','endereco']

class PerfilSupervisor(forms.ModelForm):
    class Meta:
        model = Supervisor
        fields = ['nome', 'cpf']

class FormProduto(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome','codigo','qtde_estoque','preco', 'image']

class formMeta(forms.ModelForm):
    class Meta:
        model = Meta
        fields = ['valor','desconto']