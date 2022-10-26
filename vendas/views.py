import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import sweetify
from django.http import JsonResponse
import json
from .models import *
from .utils import  dadosCarrinho

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


from vendas.models import Pedido
from .forms import *

import logging

logger = logging.getLogger(__name__)


def home(request):
    if request.user.is_authenticated:
        return render(request, 'vendas/home.html')
    else:
        sweetify.error(
            request, 'É necessário fazer login para acessar essa pagina!')
        return redirect('login')


@login_required
def perfil(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		try:
			p_form = PerfilRevendedor(
			request.POST, instance=request.user.revendedor)
		except:
			p_form = PerfilRevendedor(request.POST)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			form = p_form.save(commit=False)
			form.user = request.user
			p_form.save()
   
			sweetify.success(request, 'Seus dados foram atualizados')
			return redirect('perfil')
		else:
			sweetify.error(request, 'Houve um erro na atualização dos dados')
			return redirect('perfil')

	else:
		u_form = UserUpdateForm(instance=request.user)
		try:
			p_form = PerfilRevendedor(instance=request.user.revendedor)
		except:
			p_form = PerfilRevendedor()

	context = {
	'u_form': u_form,
	'p_form': p_form
	}

	return render(request, 'vendas/perfil.html', context)

@login_required
def produtos(request):
	try:
		request.user.revendedor
	except:
		sweetify.error(request, 'Profavor cadastre seus dados antes de fazer um pedido')
		return redirect('perfil')

	dados = dadosCarrinho(request)
 
	itensCarrinho = dados['itensCarrinho']
	pedido = dados['pedido']
	itens = dados['itens']

	produtos = Produto.objects.all()
	context = {'produtos': produtos, 'itensCarrinho': itensCarrinho}
	return render(request, 'vendas/produtos.html', context)


def carrinho(request):
    data = dadosCarrinho(request)

    itensCarrinho = data['itensCarrinho']
    pedido = data['pedido']
    itens = data['itens']
    
    context = {'itens': itens, 'pedido': pedido,
               'itensCarrinho': itensCarrinho}
    return render(request, 'vendas/carrinho.html', context)


def checkout(request):
    data = dadosCarrinho(request)

    itensCarrinho = data['itensCarrinho']
    pedido = data['pedido']
    itens = data['itens']

    context = {'itens': itens, 'pedido': pedido,
               'itensCarrinho': itensCarrinho}
    return render(request, 'vendas/checkout.html', context)


def atualizarItem(request):
    data = json.loads(request.body)
    idProduto = data['idProduto']
    action = data['action']
    print('Action:', action)
    print('Product:', idProduto)

    revendedor = request.user.revendedor
    produto = Produto.objects.get(id=idProduto)
    pedido, created = Pedido.objects.get_or_create(revendedor=revendedor, completo=False)

    itemPedido, created = ItemPedido.objects.get_or_create(
        pedido=pedido, produto=produto)

    if action == 'add':
        itemPedido.quantidade = (itemPedido.quantidade + 1)
    elif action == 'remove':
        itemPedido.quantidade = (itemPedido.quantidade - 1)

    itemPedido.save()

    if itemPedido.quantidade <= 0:
        itemPedido.delete()

    return JsonResponse('Item adicionado', safe=False)


def processarPedido(request):
    cod_pedido = datetime.datetime.now().timestamp()
    dados = json.loads(request.body)
    logger.warning('Dados:' + str(dados))

    
    if request.user.is_authenticated:
        revendedor = request.user.revendedor
        pedido, criado = Pedido.objects.get_or_create(revendedor=revendedor, completo=False)

    total = float(dados['form']['total'].replace(',', '.'))
    pedido.cod_pedido = cod_pedido
    
    

    if total == pedido.get_carrinho_total:
        pedido.status = 'aprovacao_pendente'
        pedido.completo = True
    pedido.save()
    
    sweetify.success(request,'Pedido feito com sucesso!')

    return JsonResponse('Pedido sucedido', safe=False)

def mostrarPedidos(request):
    pedidos = Pedido.objects.filter(revendedor=request.user.revendedor)
    return render(request, "vendas/meus_pedidos.html", {'pedidos': pedidos})

class detalhePedido(DetailView):
    model = Pedido
