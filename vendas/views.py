import datetime
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import sweetify
from django.views.generic import ListView
from django.http import JsonResponse
import json
from .models import * 
from .utils import cookieCarrinho, dadosCarrinho
import logging



from vendas.models import Pedido
from .forms import *


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
        p_form = PerfilRevendedor(request.POST,
                                  instance=request.user.revendedor)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            sweetify.success(request, 'Your account has been updated!')
            return redirect('perfil')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = PerfilRevendedor(instance=request.user.revendedor)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'vendas/perfil.html', context)


def produtos(request):
	dados = dadosCarrinho(request)

	itensCarrinho = dados['itensCarrinho']
	pedido = dados['pedido']
	itens = dados['itens']

	produtos = Produto.objects.all()
	context = {'produtos':produtos, 'itensCarrinho':itensCarrinho}
	return render(request, 'vendas/produtos.html', context)

def carrinho(request):
	data = dadosCarrinho(request)

	itensCarrinho = data['itensCarrinho']
	pedido = data['pedido']
	itens = data['itens']

	context = {'itens':itens, 'pedido':pedido, 'itensCarrinho':itensCarrinho}
	return render(request, 'vendas/carrinho.html', context)

def checkout(request):
	data = dadosCarrinho(request)
	
	itensCarrinho = data['itensCarrinho']
	pedido = data['pedido']
	itens = data['itens']

	context = {'itens':itens, 'pedido':pedido, 'itensCarrinho':itensCarrinho}
	return render(request, 'vendas/checkout.html', context)

def atualizarItem(request):
	data = json.loads(request.body)
	idProduto = data['idProduto']
	action = data['action']
	print('Action:', action)
	print('Product:', idProduto)

	revendedor = request.user
	produto = Produto.objects.get(id=idProduto)
	pedido, created = Pedido.objects.get_or_create(revendedor=revendedor)

	itemPedido, created = ItemPedido.objects.get_or_create(pedido=pedido, produto=produto)

	if action == 'add':
		itemPedido.quantidade = (itemPedido.quantidade + 1)
	elif action == 'remove':
		itemPedido.quantidade = (itemPedido.quantidade - 1)

	itemPedido.save()

	if itemPedido.quantidade <= 0:
		itemPedido.delete()

	return JsonResponse('Item adicionado', safe=False)