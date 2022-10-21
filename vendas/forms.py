from django import forms
from .models import Revendedor, Pedido, Item_pedido
from users.models import User


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email']
        
        
class PerfilRevendedor(forms.ModelForm):
    class Meta:
        model = Revendedor
        fields =['nome','cpf','telefone','endereco','datanasc','is_aprovado',]
        

class FormPedido(forms.ModelForm):       
    class Meta:
        model = Pedido
        fields = '__all__'
        
class FormItemPedido(forms.ModelForm):
    class meta:
        models = Item_pedido
        fields = ['produto', 'quantidade']