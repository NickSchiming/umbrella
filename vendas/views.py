from ast import For
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
import sweetify
from django.http import HttpResponse, JsonResponse
import json
from .models import *
from .utils import dadosCarrinho, renderForm, temNone
from django.db.models import Q

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

global revendedorPed
revendedorPed = None


def home(request):
    if request.user.is_authenticated:
        return render(request, 'vendas/home.html')
    else:
        sweetify.error(
            request, 'É necessário fazer login para acessar essa pagina!')
        return redirect('login')


@login_required
def perfil(request):
    if request.user.type == 'REVENDEDOR':
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            if not request.user.type == 'FRANQUIA':
                u_form.fields.pop('type')
            try:
                p_form = PerfilRevendedor(
                    request.POST, instance=request.user.revendedor)
            except:
                p_form = PerfilRevendedor(request.POST)

            if not request.user.type == 'FRANQUIA' or not request.user.type == 'SUPERVISOR':
                p_form.fields.pop('is_aprovado')

            if u_form.is_valid() and p_form.is_valid():
                if temNone(p_form):
                    sweetify.warning(
                        request, 'Preencha todos os campos para continuar')
                else:
                    u_form.save()
                    form = p_form.save(commit=False)
                    form.user = request.user
                    p_form.save()
                    sweetify.success(request, 'Seus dados foram atualizados')
                    return redirect('perfil')
            else:
                sweetify.error(
                    request, 'Houve um erro na atualização dos dados')
                return redirect('perfil')

        else:
            u_form = UserUpdateForm(instance=request.user)
            if not request.user.type == 'FRANQUIA':
                u_form.fields.pop('type')
            try:
                p_form = PerfilRevendedor(instance=request.user.revendedor)
            except:
                p_form = PerfilRevendedor()
            if not request.user.type == 'FRANQUIA' or not request.user.type == 'SUPERVISOR':
                p_form.fields.pop('is_aprovado')
    elif request.user.type == 'LOJA':
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            if not request.user.type == 'FRANQUIA':
                u_form.fields.pop('type')
            try:
                p_form = PerfilLoja(
                    request.POST, instance=request.user.revendedor)
            except:
                p_form = PerfilLoja(request.POST)

            if u_form.is_valid() and p_form.is_valid():
                if temNone(p_form):
                    sweetify.warning(
                        request, 'Preencha todos os campos para continuar')
                else:
                    u_form.save()
                    form = p_form.save(commit=False)
                    form.user = request.user
                    p_form.save()
                    sweetify.success(request, 'Seus dados foram atualizados')
                    return redirect('perfil')
            else:
                sweetify.error(
                    request, 'Houve um erro na atualização dos dados')
                return redirect('perfil')

        else:
            u_form = UserUpdateForm(instance=request.user)
            if not request.user.type == 'FRANQUIA':
                u_form.fields.pop('type')
            try:
                p_form = PerfilLoja(instance=request.user.loja)
            except:
                p_form = PerfilLoja()
    
    elif request.user.type == 'SUPERVISOR':
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            if not request.user.type == 'FRANQUIA':
                u_form.fields.pop('type')
            try:
                p_form = PerfilSupervisor(
                    request.POST, instance=request.user.revendedor)
            except:
                p_form = PerfilSupervisor(request.POST)

            if u_form.is_valid() and p_form.is_valid():
                if temNone(p_form):
                    sweetify.warning(
                        request, 'Preencha todos os campos para continuar')
                else:
                    u_form.save()
                    form = p_form.save(commit=False)
                    form.user = request.user
                    p_form.save()
                    sweetify.success(request, 'Seus dados foram atualizados')
                    return redirect('perfil')
            else:
                sweetify.error(
                    request, 'Houve um erro na atualização dos dados')
                return redirect('perfil')

        else:
            u_form = UserUpdateForm(instance=request.user)
            if not request.user.type == 'FRANQUIA':
                u_form.fields.pop('type')
            try:
                p_form = PerfilSupervisor(instance=request.user.supervisor)
            except:
                p_form = PerfilSupervisor()
    elif request.user.type == 'FRANQUIA':
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            if not request.user.type == 'FRANQUIA':
                u_form.fields.pop('type')
            try:
                p_form = PerfilFranquia(
                    request.POST, instance=request.user.revendedor)
            except:
                p_form = PerfilFranquia(request.POST)

            if u_form.is_valid() and p_form.is_valid():
                if temNone(p_form):
                    sweetify.warning(
                        request, 'Preencha todos os campos para continuar')
                else:
                    u_form.save()
                    form = p_form.save(commit=False)
                    form.user = request.user
                    p_form.save()
                    sweetify.success(request, 'Seus dados foram atualizados')
                    return redirect('perfil')
            else:
                sweetify.error(
                    request, 'Houve um erro na atualização dos dados')
                return redirect('perfil')

        else:
            u_form = UserUpdateForm(instance=request.user)
            try:
                p_form = PerfilFranquia(instance=request.user.franquia)
            except:
                p_form = PerfilFranquia()

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'vendas/perfil.html', context)

# def aprovado_check(user):
#     return user.revendedor.is_aprovado

@login_required
# @user_passes_test(aprovado_check, login_url='vendas-home')
def produtos(request):
    print(revendedorPed)
    if request.user.type == "REVENDEDOR":
        try:
            request.user.revendedor
        except:
            sweetify.error(
                request, 'Porfavor cadastre seus dados antes de fazer um pedido')
            return redirect('perfil')
    elif request.user.type == "LOJA":
        try:
            request.user.loja
        except:
            sweetify.error(
                request, 'Porfavor cadastre seus dados antes de fazer um pedido')
            return redirect('perfil')
    else:
        if revendedorPed == None:
            sweetify.error(request, 'Selecione um pedido para poder altera-lo')
            return redirect('pedidos')
    
    dados = dadosCarrinho(request, revendedorPed)

    itensCarrinho = dados['itensCarrinho']
    pedido = dados['pedido']
    itens = dados['itens']

    produtos = Produto.objects.all()
    context = {'produtos': produtos, 'itensCarrinho': itensCarrinho}

    if request.user.type == "REVENDEDOR":
        if request.user.revendedor.is_aprovado:
            return render(request, 'vendas/produtos.html', context)
        else:
            sweetify.warning(request, 'por favor aguarde o cadastro ser aprovado')
            return redirect('vendas-home')
    else:
        return render(request, 'vendas/produtos.html', context)
        


def carrinho(request):
    data = dadosCarrinho(request, revendedorPed)

    itensCarrinho = data['itensCarrinho']
    pedido = data['pedido']
    itens = data['itens']

    context = {'itens': itens, 'pedido': pedido,
               'itensCarrinho': itensCarrinho}
    return render(request, 'vendas/carrinho.html', context)


def checkout(request):
    data = dadosCarrinho(request, revendedorPed)

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
    if request.user.type == 'REVENDEDOR':
        revendedor = request.user.revendedor
        pedido, created = Pedido.objects.get_or_create(
        revendedor=revendedor, completo=False)
    elif request.user.type == 'LOJA':
        loja = request.user.loja
        pedido, created = Pedido.objects.get_or_create(
        loja=loja, completo=False)
    else:
        revendedor = revendedorPed
        try:
            pedido, created = Pedido.objects.get_or_create(
            revendedor=revendedor, completo=False)
        except:
            pedido, created = Pedido.objects.get_or_create(
            loja=revendedor, completo=False)
    produto = Produto.objects.get(id=idProduto)
    

    itemPedido, created = ItemPedido.objects.get_or_create(
        pedido=pedido, produto=produto)

    if action == 'add':
        itemPedido.quantidade = (itemPedido.quantidade + 1)
    elif action == 'remove':
        itemPedido.quantidade = (itemPedido.quantidade - 1)
    else:
        itemPedido.quantidade = int(action)

    itemPedido.save()

    if itemPedido.quantidade <= 0:
        itemPedido.delete()

    sweetify.success(request, 'Carrinho atualizado!',
                     position='top-end', timer=1000, toast=True, width='fit-content')
    return JsonResponse('Item adicionado', safe=False)


def processarPedido(request):
    cod_pedido = str(datetime.datetime.now().timestamp())
    dados = json.loads(request.body)

    if request.user.is_authenticated:
        if request.user.type == 'REVENDEDOR':
            revendedor = request.user.revendedor
            pedido, criado = Pedido.objects.get_or_create(
                revendedor=revendedor, completo=False)
        elif request.user.type == 'LOJA':
            loja = request.user.loja
            pedido, criado = Pedido.objects.get_or_create(
                loja=loja, completo=False)
        else:
            revendedor = revendedorPed
            try:
                pedido, criado = Pedido.objects.get_or_create(
                    revendedor=revendedor, completo=False)
            except:
                    pedido, criado = Pedido.objects.get_or_create(
                    loja=revendedor, completo=False)

    total = float(dados['form']['total'].replace(',', '.'))
    pedido.cod_pedido = cod_pedido

    pgto = dados['form']['formaPgto']

    if total == pedido.get_carrinho_total:
        pedido.status = pedido.APROV_PEND
        pedido.metodo_de_pagamento = pgto
        pedido.completo = True

    estoque = pedido.falta_estoque()

    if estoque[0]:
        sweetify.error(request, 'O produto ' +
                       estoque[1] + ' está em falta no momento')
        return JsonResponse('Falta de estoque', safe=False)
    else:
        pedido.baixa_estoque()
        pedido.save()
        sweetify.success(request, 'Pedido feito com sucesso!')
        return JsonResponse('Pedido sucedido', safe=False)


def mostrarPedidos(request):
    if request.user.type == 'REVENDEDOR':
        try:
            request.user.revendedor
        except:
            sweetify.error(
                request, 'Porfavor cadastre seus dados antes de fazer um pedido')
            return redirect('perfil')
        pedidos = Pedido.objects.filter(revendedor=request.user.revendedor).exclude(
            completo=False).order_by('-data')
    elif request.user.type == 'LOJA':
        try:
            request.user.loja
        except:
            sweetify.error(
                request, 'Porfavor cadastre seus dados antes de fazer um pedido')
            return redirect('perfil')
        pedidos = Pedido.objects.filter(loja=request.user.loja).exclude(
            completo=False).order_by('-data')

    return render(request, "vendas/meus_pedidos.html", {'pedidos': pedidos})


def detalhePedido(request, pk):
    pedido = Pedido.objects.get(id=pk)
    itens = pedido.itempedido_set.all()

    return render(request, "vendas/detalhe_pedido.html", {'pedido': pedido, 'itens': itens})


def atualizarPedido(request, pk):
    if request.user.type == "REVENDEDOR":
        pedido = Pedido.objects.get(id=pk)
        pedido_ex = Pedido.objects.get(
            revendedor=request.user.revendedor, completo=False)
        pedido_ex.delete()
        pedido.completo = False
        pedido.devolve_produtos()
        pedido.save()
        sweetify.success(
            request, 'Por favor altere o pedido a faça checkout novamente')
        return redirect('produtos')
    elif request.user.type == "LOJA":
        pedido = Pedido.objects.get(id=pk)
        pedido_ex = Pedido.objects.get(
            loja=request.user.loja, completo=False)
        pedido_ex.delete()
        pedido.completo = False
        pedido.devolve_produtos()
        pedido.save()
        sweetify.success(
            request, 'Por favor altere o pedido a faça checkout novamente')
        return redirect('produtos')
    else:
        global revendedorPed
        try:
            print('revendedor: ' + str(pedido.revendedor))
            pedido = Pedido.objects.get(id=pk)
            pedido_ex = Pedido.objects.get(
                revendedor=pedido.revendedor, completo=False)
            revendedorPed = pedido.revendedor
            pedido_ex.delete()
            pedido.completo = False
            pedido.devolve_produtos()
            pedido.save()
            sweetify.success(
                request, 'Por favor altere o pedido a faça checkout novamente')
            return redirect('produtos')
        except:
            pedido = Pedido.objects.get(id=pk)
            pedido_ex = Pedido.objects.get(
                loja=pedido.loja, completo=False)
            print('loja: ' + str(pedido.loja))
            revendedorPed = pedido.loja
            pedido_ex.delete()
            pedido.completo = False
            pedido.devolve_produtos()
            pedido.save()
            sweetify.success(
                request, 'Por favor altere o pedido a faça checkout novamente')
            return redirect('produtos')

def deletarPedido(request, pk):
    pedido = Pedido.objects.get(id=pk)
    pedido.devolve_produtos()
    pedido.delete()
    sweetify.success(request, 'Pedido excluido com sucesso')
    return redirect('pedidos')


def lista_usuarios(request):
    usuarios = User.objects.all()
    return render(request, "vendas/usuarios.html", {'usuarios': usuarios})


def atualizarUsuario(request, pk):
    user = User.objects.get(id=pk)
    context = renderForm(request, user)
    if context['reload']:
        del context['reload']
        return redirect(request.path_info)
    else:
        del context['reload']

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

def atualizarProduto(request, pk):
    produto = Produto.objects.get(id=pk)

    if request.method == 'POST':
        form = FormProduto(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            sweetify.success(request, 'Produto atualizados')
        else:
            sweetify.error(request, 'Houve um erro na atualização dos dados')
    else:
        form = FormProduto(instance=produto)

    return render(request, 'vendas/dados_produtos.html', {'form': form, 'produto': produto})


def deletarProduto(request, pk):
    produto = Produto.objects.get(id=pk)
    produto.delete()
    return redirect('produtos')

def aprovarPedido(request, pk):
    pedido = Pedido.objects.get(id=pk)
    pedido.status = 'APROVADO'
    pedido.save()
    sweetify.success(request, 'Pedido aprovado!')
    return redirect('pedidos')

def enviarPedido(request, pk):
    if pedido.status == 'APROVADO':
        pedido = Pedido.objects.get(id=pk)
        pedido.status = 'ENVIADO'
        pedido.save()
        sweetify.success(request, 'Pedido enviado!')
        return redirect('pedidos')
    else:
        sweetify.error(request, 'O pedido ainda não foi aprovado!')

def confirmarPedido(request, pk):
    if pedido.status == 'ENVIADO':
        pedido = Pedido.objects.get(id=pk)
        pedido.status = 'FINALIZADO'
        pedido.save()
        sweetify.success(request, 'Pedido finalizado!')
        return redirect('pedidos')
    else:
        sweetify.error(request, 'O pedido ainda não foi enviado!')

class pesquisaUsuarios(ListView):
    model = User

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = User.objects.filter(
            Q(email__icontains=query)
        )
        return object_list

class pesquisaPedidos(ListView):
    model = Pedido


    def get_queryset(self):
        query = self.request.GET.get("q")
        if self.request.user.type == 'REVENDEDOR':
            object_list = Pedido.objects.filter(Q(revendedor=self.request.user.revendedor),
                Q(cod_pedido__icontains=query) | Q(status__icontains=query)
                | Q(metodo_de_pagamento__icontains=query) | Q(data__year=query)
                | Q(data__month=query) | Q(data__day=query)
            )
        elif self.request.user.type == 'LOJA':
            object_list = Pedido.objects.filter(Q(loja=self.request.user.loja),
                Q(cod_pedido__icontains=query) | Q(status__icontains=query)
                | Q(metodo_de_pagamento__icontains=query) | Q(data__year=query)
                | Q(data__month=query) | Q(data__day=query)
            )
        else:
            object_list = Pedido.objects.filter(
                Q(cod_pedido__icontains=query) | Q(status__icontains=query)
                | Q(metodo_de_pagamento__icontains=query) | Q(data__year=query)
                | Q(data__month=query) | Q(data__day=query)
            )
        return object_list

class pesquisaProdutos(ListView):
    model = Produto

    def get_context_data(self, **kwargs):
        context = super(pesquisaProdutos, self).get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        return context

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Produto.objects.filter(
            Q(codigo__icontains=query) | Q(nome__icontains=query)
        )

        return object_list
