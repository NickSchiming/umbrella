from ast import For
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import sweetify
from django.http import HttpResponse, JsonResponse
import json
from .models import *
from .utils import  dadosCarrinho, renderForm

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

        logger.warning(u_form)
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
        if not request.user.type == 'FRANQUIA':
            u_form.fields.pop('type')
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
		sweetify.error(request, 'Porfavor cadastre seus dados antes de fazer um pedido')
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

    sweetify.success(request, 'item adicionado', position='top-end', timer=1000, toast=True, width='10%')
    return JsonResponse('Item adicionado', safe=False)


def processarPedido(request):
    cod_pedido = datetime.datetime.now().timestamp()
    dados = json.loads(request.body)
    

    
    if request.user.is_authenticated:
        revendedor = request.user.revendedor
        pedido, criado = Pedido.objects.get_or_create(revendedor=revendedor, completo=False)

    total = float(dados['form']['total'].replace(',', '.'))
    pedido.cod_pedido = cod_pedido
    
    pgto = dados['form']['formaPgto']

    if total == pedido.get_carrinho_total:
        pedido.status = pedido.APROV_PEND
        pedido.metodo_de_pagamento = pgto
        pedido.completo = True
    
    estoque = pedido.falta_estoque()

    if estoque[0]:
        sweetify.error(request, 'O produto ' + estoque[1] + ' está em falta no momento')
        return JsonResponse('Falta de estoque', safe=False)
    else:
        pedido.baixa_estoque()
        pedido.save()
        sweetify.success(request,'Pedido feito com sucesso!')
        return JsonResponse('Pedido sucedido', safe=False)

def mostrarPedidos(request):
    try:
     request.user.revendedor
    except:
        sweetify.error(request, 'Porfavor cadastre seus dados antes de fazer um pedido')
        return redirect('perfil')
    pedidos = Pedido.objects.filter(revendedor=request.user.revendedor).exclude(completo=False).order_by('-data')

    return render(request, "vendas/meus_pedidos.html", {'pedidos': pedidos})

def detalhePedido(request, pk):
    pedido = Pedido.objects.get(id=pk)
    itens = pedido.itempedido_set.all()

    return render(request, "vendas/detalhe_pedido.html", {'pedido': pedido, 'itens' : itens})

def atualizarPedido(request, pk):
    pedido = Pedido.objects.get(id=pk)
    pedido_ex = Pedido.objects.get(revendedor=request.user.revendedor, completo=False)
    pedido_ex.delete()
    pedido.completo = False
    pedido.devolve_produtos()
    pedido.save()
    sweetify.success(request, 'Por favor altere o pedido a faça checkout novamente')
    return redirect('produtos')


def deletarPedido(request, pk):
    pedido = Pedido.objects.get(id=pk)
    pedido.devolve_produtos()
    pedido.delete()
    sweetify.success(request, 'Pedido excluido com sucesso')
    return redirect('vendas-home')

def lista_usuarios(request):
    usuarios = User.objects.all()
    return render(request, "vendas/usuarios.html", {'usuarios': usuarios})

def atualizarUsuario(request, pk):
    user = User.objects.get(id=pk)
    context = renderForm(request, user)
    return render(request, 'vendas/perfil.html', context)


def deletarUsuario(request, pk):
    user = User.objects.get(id=pk)
    user.delete()
    sweetify.success(request, 'Usuario excluido com sucesso')
    return redirect('usuarios')

def lista_pedidos(request):
    pedidos = Pedido.objects.all().exclude(completo=False)
    return render(request, "vendas/pedidos.html", {'pedidos': pedidos})

def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, "vendas/cadastro_produtos.html", {'produtos': produtos})

def deletarPedido(request, pk):
    pedido = Pedido.objects.get(id=pk)
    pedido.delete()
    return redirect('pedidos')

def atualizarProduto(request, pk):
    produto = Produto.objects.get(id=pk)

    if request.method == 'POST':
        form = FormProduto(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            sweetify.success(request, 'Produto atualizados')
            return redirect('produtos')
        else:
            sweetify.error(request, 'Houve um erro na atualização dos dados')
            return redirect('produtos')
    else:
        form = FormProduto(instance=produto)

    return render(request, 'vendas/dados_produtos.html', {'form': form, 'produto':produto})

def deletarProduto(request, pk):
    produto = Produto.objects.get(id=pk)
    produto.delete()
    return redirect('produtos')