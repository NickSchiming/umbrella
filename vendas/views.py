import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
import sweetify
from django.http import JsonResponse
import json
from .models import *
from .utils import dadosCarrinho, renderForm, temNone
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

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


def supervisor_check(user):
    if user.type == 'SUPERVISOR':
        return True
    else:
        return False


def supervisor_franquia_check(user):
    if user.type == 'SUPERVISOR' or user.type == 'FRANQUIA':
        return True
    else:
        return False


def franquia_check(user):
    if user.type == 'FRANQUIA':
        return True
    else:
        return False


@login_required
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


@login_required
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
            sweetify.info(request, 'por favor aguarde o cadastro ser aprovado')
            return redirect('vendas-home')
    else:
        return render(request, 'vendas/produtos.html', context)


@login_required
def carrinho(request):
    data = dadosCarrinho(request, revendedorPed)

    itensCarrinho = data['itensCarrinho']
    pedido = data['pedido']
    itens = data['itens']

    context = {'itens': itens, 'pedido': pedido,
               'itensCarrinho': itensCarrinho}
    return render(request, 'vendas/carrinho.html', context)


@login_required
def checkout(request):
    data = dadosCarrinho(request, revendedorPed)

    itensCarrinho = data['itensCarrinho']
    pedido = data['pedido']
    itens = data['itens']

    context = {'itens': itens, 'pedido': pedido,
               'itensCarrinho': itensCarrinho}
    return render(request, 'vendas/checkout.html', context)


@login_required
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


@login_required
def processarPedido(request):
    cod_pedido = str(datetime.datetime.now().timestamp())
    dados = json.loads(request.body)
    global revendedorPed

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

    subtotal = float(dados['form']['subtotal'].replace(',', '.'))
    total = float(dados['form']['total'].replace(',', '.'))
    pedido.cod_pedido = cod_pedido

    pgto = dados['form']['formaPgto']

    if total == pedido.get_meta_total:
        if request.user.type == 'REVENDEDOR':
            pedido.status = pedido.APROV_PEND
        else:
            pedido.status = pedido.APROVADO
        pedido.metodo_de_pagamento = pgto
        pedido.subtotal = subtotal
        pedido.total = total
        if pedido.revendedor:
            pedido.franquia = pedido.revendedor.supervisor.franquia
        elif pedido.loja:
            pedido.franquia = pedido.loja.franquia
        pedido.completo = True

    estoque = pedido.falta_estoque()

    if estoque[0]:
        sweetify.error(request, 'O produto ' +
                       estoque[1] + ' está em falta no momento')
        return JsonResponse('Falta de estoque', safe=False)
    else:
        revendedorPed = None
        pedido.baixa_estoque()
        pedido.save()
        sweetify.success(request, 'Pedido feito com sucesso!')
        return JsonResponse('Pedido sucedido', safe=False)


@login_required
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


@login_required
def detalhePedido(request, pk):
    pedido = Pedido.objects.get(id=pk)
    itens = pedido.itempedido_set.all()

    return render(request, "vendas/detalhe_pedido.html", {'pedido': pedido, 'itens': itens})


@login_required
def atualizarPedido(request, pk):
    if request.user.type == "REVENDEDOR":
        pedido = Pedido.objects.get(id=pk)
        pedido_ex = Pedido.objects.get(
            revendedor=request.user.revendedor, completo=False)
        pedido_ex.delete()
        pedido.completo = False
        pedido.devolve_produtos()
        pedido.save()
        sweetify.info(
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
        sweetify.info(
            request, 'Por favor altere o pedido a faça checkout novamente')
        return redirect('produtos')
    else:
        global revendedorPed
        pedido = Pedido.objects.get(id=pk)
        if request.user.type == 'FRANQUIA' or request.user.type == 'SUPERVISOR':
            if pedido.revendedor:
                revendedor = pedido.revendedor
                revendedorPed = pedido.revendedor
                pedido.completo = False
                pedido.devolve_produtos()
                pedido.save()
                sweetify.info(
                    request, 'Por favor altere o pedido a faça checkout novamente')
                return redirect('produtos')
            else:
                loja = pedido.loja
                revendedorPed = pedido.loja
                pedido.completo = False
                pedido.devolve_produtos()
                pedido.save()
                sweetify.info(
                    request, 'Por favor altere o pedido a faça checkout novamente')
                return redirect('produtos')
        else:
            if pedido.revendedor:
                revendedor = pedido.revendedor
                pedido_ex = Pedido.objects.get(
                    revendedor=revendedor, completo=False)
                print('revendedor: ' + str(pedido.revendedor))
                revendedorPed = pedido.revendedor
                pedido_ex.delete()
                pedido.completo = False
                pedido.devolve_produtos()
                pedido.save()
                sweetify.info(
                    request, 'Por favor altere o pedido a faça checkout novamente')
                return redirect('produtos')
            else:
                loja = pedido.loja
                pedido_ex = Pedido.objects.get(
                    loja=loja, completo=False)
                print('loja: ' + str(pedido.loja))
                revendedorPed = pedido.loja
                pedido_ex.delete()
                pedido.completo = False
                pedido.devolve_produtos()
                pedido.save()
                sweetify.info(
                    request, 'Por favor altere o pedido a faça checkout novamente')
                return redirect('produtos')


@login_required
def deletarPedido(request, pk):
    pedido = Pedido.objects.get(id=pk)
    pedido.devolve_produtos()
    pedido.delete()
    sweetify.success(request, 'Pedido excluido com sucesso')
    return redirect('pedidos')


@login_required
@user_passes_test(supervisor_franquia_check)
def lista_usuarios(request):
    usuarios = User.objects.all()
    return render(request, "vendas/usuarios.html", {'usuarios': usuarios})


@login_required
@user_passes_test(supervisor_franquia_check)
def atualizarUsuario(request, pk):
    user = User.objects.get(id=pk)
    context = renderForm(request, user)
    if context['reload']:
        del context['reload']
        return redirect(request.path_info)
    else:
        del context['reload']

    return render(request, 'vendas/perfil.html', context)


@login_required
@user_passes_test(supervisor_franquia_check)
def deletarUsuario(request, pk):
    user = User.objects.get(id=pk)
    user.delete()
    sweetify.success(request, 'Usuario excluido com sucesso')
    return redirect('usuarios')


@login_required
@user_passes_test(supervisor_franquia_check)
def lista_pedidos(request):
    pedidos = Pedido.objects.all().exclude(completo=False)
    return render(request, "vendas/pedidos.html", {'pedidos': pedidos})


@login_required
@user_passes_test(supervisor_franquia_check)
def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, "vendas/cadastro_produtos.html", {'produtos': produtos})


@login_required
@user_passes_test(supervisor_franquia_check)
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


@login_required
@user_passes_test(supervisor_franquia_check)
def adicionarProduto(request):

    if request.method == 'POST':
        form = FormProduto(request.POST)
        if form.is_valid():
            form.save()
            sweetify.success(request, 'Produto adicionado')
        else:
            sweetify.error(request, 'Houve um erro na atualização dos dados')
    else:
        form = FormProduto()
    return render(request, 'vendas/dados_produtos.html', {'form': form})


@login_required
@user_passes_test(supervisor_franquia_check)
def deletarProduto(request, pk):
    produto = Produto.objects.get(id=pk)
    produto.delete()
    return redirect('cadastro_produtos')


@login_required
@user_passes_test(supervisor_check)
def aprovarPedido(request, pk):
    pedido = Pedido.objects.get(id=pk)
    pedido.status = 'APROVADO'
    pedido.save()
    sweetify.success(request, 'Pedido aprovado!')
    return redirect('pedidos')


@login_required
@user_passes_test(franquia_check)
def enviarPedido(request, pk):
    if pedido.status == 'APROVADO':
        pedido = Pedido.objects.get(id=pk)
        pedido.status = 'ENVIADO'
        pedido.save()
        sweetify.success(request, 'Pedido enviado!')
        return redirect('pedidos')
    else:
        sweetify.error(request, 'O pedido ainda não foi aprovado!')


@login_required
def confirmarPedido(request, pk):
    if pedido.status == 'ENVIADO':
        pedido = Pedido.objects.get(id=pk)
        pedido.status = 'FINALIZADO'
        pedido.save()
        sweetify.success(request, 'Pedido finalizado!')
        return redirect('pedidos')
    else:
        sweetify.error(request, 'O pedido ainda não foi enviado!')


class pesquisaUsuarios(LoginRequiredMixin, ListView):
    model = User

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = User.objects.filter(
            Q(email__icontains=query)
        )
        return object_list


class pesquisaPedidos(LoginRequiredMixin, ListView):
    model = Pedido

    def get_queryset(self):
        query = self.request.GET.get("q")
        if self.request.user.type == 'REVENDEDOR':
            object_list = Pedido.objects.filter(Q(revendedor=self.request.user.revendedor),
                                                Q(cod_pedido__icontains=query) | Q(
                                                    status__icontains=query)
                                                | Q(metodo_de_pagamento__icontains=query) | Q(data__year=query)
                                                | Q(data__month=query) | Q(data__day=query)
                                                )
        elif self.request.user.type == 'LOJA':
            object_list = Pedido.objects.filter(Q(loja=self.request.user.loja),
                                                Q(cod_pedido__icontains=query) | Q(
                                                    status__icontains=query)
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


class pesquisaProdutos(LoginRequiredMixin, ListView):
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


@login_required
@user_passes_test(franquia_check)
def metas(request):
    metas = Meta.objects.all()
    return render(request, "vendas/metas.html", {'metas': metas})


@login_required
@user_passes_test(franquia_check)
def atualizarMeta(request, pk):
    meta = Meta.objects.get(id=pk)
    if request.method == 'POST':
        form = formMeta(request.POST, instance=meta)
        if form.is_valid():
            form.save()
            sweetify.success(
                request, 'Meta atualizada!')
    else:
        form = formMeta(instance=meta)
    return render(request, 'vendas/atualizar_meta.html', {'form': form})


@login_required
@user_passes_test(franquia_check)
def atualizarMetasRevendedores(request):

    revendedores = Revendedor.objects.all()
    bronze, prata, ouro, diamante = Meta.objects.all()

    for revendedor in revendedores:
        if revendedor.total_comprado <= bronze.valor:
            revendedor.meta = bronze
        elif revendedor.total_comprado <= prata.valor:
            revendedor.meta = prata
        elif revendedor.total_comprado <= ouro.valor:
            revendedor.meta = ouro
        else:
            revendedor.meta = diamante
        revendedor.save()

    return redirect('metas')


def atualizarRelatorio(request):
    dados = json.loads(request.body)

    acao = dados['action']
    request.session['acao'] = acao

    return JsonResponse('feito', safe=False)


def relatorios(request):
    now = datetime.datetime.now()
    acao = request.session.get('acao')
    """ itenspedido = [] """
    pedidos = request.user.franquia.pedido_set.all()
    """ for pedido in pedidos:
        itenspedido += pedido.itempedido_set.all()
        
    for item in itenspedido:
        item.nome """
    soma = 0

    if acao == 'dia':
        pedidos = request.user.franquia.pedido_set.filter(data__day=now.day)
        supervisores = request.user.franquia.supervisor_set.all()
        """ for supervisor in supervisores:
            soma += supervisor.revendedor_set.filter(data__day=now.day).count() """
        qtde_pedidos_aprovados = pedidos.filter(
            status='APROVADO', data__day=now.day).count()
        qtde_pedidos_enviados = pedidos.filter(
            status='ENVIADOS', data__day=now.day).count()
        qtde_pedidos_finalizados = pedidos.filter(
            status='FINALIZADOS', data__day=now.day).count()
    elif acao == 'mes':
        pedidos = request.user.franquia.pedido_set.filter(
            data__month=now.month)
        supervisores = request.user.franquia.supervisor_set.all()
        """ for supervisor in supervisores:
            soma += supervisor.revendedor_set.filter(
                data__month=now.month).count() """
        qtde_pedidos_aprovados = pedidos.filter(
            status='APROVADO', data__month=now.month).count()
        qtde_pedidos_enviados = pedidos.filter(
            status='ENVIADOS', data__month=now.month).count()
        qtde_pedidos_finalizados = pedidos.filter(
            status='FINALIZADOS', data__month=now.month).count()
    elif acao == 'ano':
        pedidos = request.user.franquia.pedido_set.filter(data__year=now.year)
        supervisores = request.user.franquia.supervisor_set.all()
        """ for supervisor in supervisores:
            soma += supervisor.revendedor_set.filter(
                data__year=now.year).count() """
        qtde_pedidos_aprovados = pedidos.filter(
            status='APROVADO', data__year=now.year).count()
        qtde_pedidos_enviados = pedidos.filter(
            status='ENVIADOS', data__year=now.year).count()
        qtde_pedidos_finalizados = pedidos.filter(
            status='FINALIZADOS', data__year=now.year).count()

    total = sum([pedido.get_meta_total for pedido in pedidos])
    qtde_pedidos = pedidos.count()
    qtde_pedidos_aprovados = pedidos.filter(status='APROVADO').count()
    qtde_pedidos_enviados = pedidos.filter(status='ENVIADOS').count()
    qtde_pedidos_finalizados = pedidos.filter(status='FINALIZADOS').count()

    context = {'total': total,
               'revendedores': soma,
               'qtde_pedidos': qtde_pedidos,
               'qtde_pedidos_aprovados': qtde_pedidos_aprovados,
               'qtde_pedidos_enviados': qtde_pedidos_enviados,
               'qtde_pedidos_finalizados': qtde_pedidos_finalizados}

    return render(request, 'vendas/relatorios.html', context)
