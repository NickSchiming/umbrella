from django import forms
from .models import Franquia, Loja, Produto, Produto, Revendedor, Pedido, ItemPedido, Supervisor
from users.models import User


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'type']
    
    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user', None)
    #     super().__init__(*args, **kwargs)
        
    #     if  user.type == 'FRANQUIA':
    #         self.fields += ['type']


class PerfilRevendedor(forms.ModelForm):
    class Meta:
        model = Revendedor
        fields = ['nome', 'cpf', 'telefone','cep',
                  'endereco', 'datanasc',]

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
        fields = ['nome','codigo','qtde_estoque','preco']