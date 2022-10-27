from django import forms
from .models import Franquia, Produto, Produto, Revendedor, Pedido, ItemPedido
from users.models import User


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email']


class PerfilRevendedor(forms.ModelForm):
    class Meta:
        model = Revendedor
        fields = ['nome', 'cpf', 'telefone','cep',
                  'endereco', 'datanasc',]

class PerfilFranquia(forms.ModelForm):
    class Meta:
        model = Franquia
        fields = ['razaosocial','cnpj','endereco']

class FormProduto(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome','codigo','qtde_estoque','preco']

