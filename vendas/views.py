import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
import sweetify
from django.http import JsonResponse
import json
from .models import *
from .utils import aprovado_check, dadosCarrinho, infoHome, perfil_u_form_get, perfil_u_form_post, renderForm, salva_p_form, temNone, tira_field_perfil_rev, verifica_perfil
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from babel.dates import format_date
from django.core import serializers

from django.views.generic import ListView

from vendas.models import Pedido
from .forms import *


def supervisor_check(user):
    if user.tipo == User.SUPERVISOR:
        return True
    else:
        return False


def supervisor_franquia_check(user):
    if user.tipo == User.SUPERVISOR or user.tipo == User.FRANQUIA:
        return True
    else:
        return False


def franquia_check(user):
    if user.tipo == User.FRANQUIA:
        return True
    else:
        return False


@login_required
def home(request):
    now = datetime.datetime.now()
    user = request.user
    context = {'user': user}

    if hasattr(user, 'revendedor'):
        pedidos = user.revendedor.pedido_set.filter(
            completo=True, data__month=now.month)
        width = str((user.revendedor.total_comprado /
                     user.revendedor.get_proxima_meta.valor) * 100) + '%'
        context = infoHome(user, pedidos)
        context['width'] = width

    elif hasattr(user, 'franquia'):
        pedidos = user.franquia.pedido_set.filter(completo=True,
                                                  data__day=now.day)
        context = infoHome(user, pedidos)

    elif hasattr(user, 'loja'):
        pedidos = user.loja.pedido_set.filter(completo=True,
                                              data__month=now.month)
        context = infoHome(user, pedidos)

    elif hasattr(user, 'supervisor'):
        pedidos = Pedido.objects.none()
        revendedores = user.supervisor.revendedor_set.all()

        users_rev = User.objects.filter(
            tipo=User.REVENDEDOR, criado__month=now.month).count()
        for revendedor in revendedores:
            pedidos = pedidos | revendedor.pedido_set.filter(completo=True,
                                                             data__month=now.month)
        context = infoHome(user, pedidos)
        context['qtde_pedidos_aprovados'] = context['qtde_pedidos_aprovados'] + \
            context['qtde_pedidos_enviados'] + \
            context['qtde_pedidos_finalizados']
        context['novos_revendedores'] = users_rev

    else:
        sweetify.info(request, 'Por favor, finalize seu cadastro!')
        return redirect('perfil')

    now = datetime.datetime.now()
    mes = format_date(now, "MMMM", locale='pt_BR').capitalize()
    context['mes'] = mes
    dia = format_date(now, "d", locale='pt_BR').capitalize()
    context['dia'] = dia

    return render(request, 'vendas/home.html', context)


@login_required
def perfil(request):
    tipo = request.user.tipo
    if tipo == User.REVENDEDOR:
        if request.method == 'POST':
            u_form = perfil_u_form_post(request)
            try:
                p_form = PerfilRevendedor(
                    request.POST, instance=request.user.revendedor)
            except:
                p_form = PerfilRevendedor(request.POST)

            salva_p_form(request, tipo, u_form, p_form)

        else:
            u_form = perfil_u_form_get(request)
            try:
                p_form = PerfilRevendedor(instance=request.user.revendedor)

            except:
                p_form = PerfilRevendedor()

    elif tipo == User.LOJA:
        if request.method == 'POST':
            u_form = perfil_u_form_post(request)
            try:
                p_form = PerfilLoja(request.POST, instance=request.user.loja)
            except:
                p_form = PerfilLoja(request.POST)

            salva_p_form(request, tipo, u_form, p_form)

        else:

            u_form = perfil_u_form_get(request)
            try:
                p_form = PerfilLoja(instance=request.user.loja)
            except:
                p_form = PerfilLoja()

    elif tipo == User.SUPERVISOR:
        if request.method == 'POST':
            u_form = perfil_u_form_post(request)
            try:
                p_form = PerfilSupervisor(
                    request.POST, instance=request.user.supervisor)
            except:
                p_form = PerfilSupervisor(request.POST)

            salva_p_form(request, tipo, u_form, p_form)

        else:

            u_form = perfil_u_form_get(request)
            try:
                p_form = PerfilSupervisor(instance=request.user.supervisor)
            except:
                p_form = PerfilSupervisor()

    elif tipo == User.FRANQUIA:
        if request.method == 'POST':
            u_form = perfil_u_form_post(request)
            try:
                p_form = PerfilFranquia(
                    request.POST, instance=request.user.franquia)
            except:
                p_form = PerfilFranquia(request.POST)

            salva_p_form(request, tipo, u_form, p_form)

        else:

            u_form = perfil_u_form_get(request)
            try:
                p_form = PerfilFranquia(instance=request.user.franquia)
            except:
                p_form = PerfilFranquia()

    tira_field_perfil_rev(request, tipo, p_form)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'vendas/perfil.html', context)


@login_required
def produtos(request):
    if verifica_perfil(request, request.session.get('revendped_id')) == 1:
        return redirect('perfil')
    elif verifica_perfil(request, request.session.get('revendped_id')) == 2:
        return redirect('pedidos')

    dados = dadosCarrinho(request, request.session.get(
        'revendped_id'), request.session.get('tipo'))

    itensCarrinho = dados['itensCarrinho']
    pedido = dados['pedido']
    itens = dados['itens']

    produtos = Produto.objects.all()
    context = {'produtos': produtos, 'itensCarrinho': itensCarrinho}

    if aprovado_check(request.user):
        return render(request, 'vendas/produtos.html', context)
    else:
        sweetify.info(request, 'por favor aguarde o cadastro ser aprovado')
        return redirect('vendas-home')


@login_required
def carrinho(request):
    if verifica_perfil(request, request.session.get('revendped_id')):
        return redirect('perfil')
    data = dadosCarrinho(request, request.session.get(
        'revendped_id'), request.session.get('tipo'))

    itensCarrinho = data['itensCarrinho']
    pedido = data['pedido']
    itens = data['itens']

    context = {'itens': itens, 'pedido': pedido,
               'itensCarrinho': itensCarrinho}
    if aprovado_check(request.user):
        return render(request, 'vendas/carrinho.html', context)
    else:
        sweetify.info(request, 'por favor aguarde o cadastro ser aprovado')
        return redirect('vendas-home')


@login_required
def checkout(request):
    data = dadosCarrinho(request, request.session.get(
        'revendped_id'), request.session.get('tipo'))

    itensCarrinho = data['itensCarrinho']
    pedido = data['pedido']
    itens = data['itens']

    context = {'itens': itens, 'pedido': pedido,
               'itensCarrinho': itensCarrinho}
    print(pedido)
    return render(request, 'vendas/checkout.html', context)


@login_required
def atualizarItem(request):
    data = json.loads(request.body)
    idProduto = data['idProduto']
    action = data['action']
    if request.user.tipo == User.REVENDEDOR:
        revendedor = request.user.revendedor
        pedido, created = Pedido.objects.get_or_create(
            revendedor=revendedor, completo=False)
    elif request.user.tipo == User.LOJA:
        loja = request.user.loja
        pedido, created = Pedido.objects.get_or_create(
            loja=loja, completo=False)
    else:
        tipo = request.session.get('tipo')
        id_revend = request.session.get('revendped_id')
        if tipo == 'revendedor':
            revendedor = Revendedor.objects.get(id=id_revend)
            pedido, created = Pedido.objects.get_or_create(
                revendedor=revendedor, completo=False)
        elif tipo == 'loja':
            loja = Loja.objects.get(id=id_revend)
            pedido, created = Pedido.objects.get_or_create(
                loja=loja, completo=False)
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
    cod_pedido = str(datetime.datetime.now().timestamp())[12:]
    dados = json.loads(request.body)

    if request.user.is_authenticated:
        if request.user.tipo == User.REVENDEDOR:
            revendedor = request.user.revendedor
            pedido, criado = Pedido.objects.get_or_create(
                revendedor=revendedor, completo=False)
        elif request.user.tipo == User.LOJA:
            loja = request.user.loja
            pedido, criado = Pedido.objects.get_or_create(
                loja=loja, completo=False)
        else:
            tipo = request.session.get('tipo')
            id_revend = request.session.get('revendped_id')
            if tipo == 'revendedor':
                revendedor = Revendedor.objects.get(id=id_revend)
                pedido, created = Pedido.objects.get_or_create(
                    revendedor=revendedor, completo=False)
            elif tipo == 'loja':
                loja = Loja.objects.get(id=id_revend)
                pedido, created = Pedido.objects.get_or_create(
                    loja=loja, completo=False)

    subtotal = float(dados['form']['subtotal'].replace(',', '.'))
    total = float(dados['form']['total'].replace(',', '.'))
    pedido.cod_pedido = cod_pedido

    pgto = dados['form']['formaPgto']

    if total == pedido.get_meta_total:
        if request.user.tipo != User.LOJA and hasattr(pedido, 'revendedor'):
            pedido.status = Pedido.APROV_PEND
        else:
            pedido.status = Pedido.APROVADO
        pedido.metodo_de_pagamento = pgto
        pedido.subtotal = subtotal
        pedido.total = total
        if pedido.revendedor == None:
            pedido.franquia = pedido.loja.franquia
        else:
            pedido.franquia = pedido.revendedor.supervisor.franquia

        pedido.completo = True

    estoque = pedido.falta_estoque()

    if estoque[0]:
        sweetify.error(request, 'O produto ' +
                       estoque[1] + ' está em falta no momento')
        return JsonResponse('Falta de estoque', safe=False)
    else:
        request.session['revendped_id'] = None
        pedido.baixa_estoque()
        pedido.save()
        sweetify.success(request, 'Pedido feito com sucesso!')
        return JsonResponse('Pedido sucedido', safe=False)


@login_required
def mostrarPedidos(request):
    if request.user.tipo == User.REVENDEDOR:
        try:
            request.user.revendedor
        except:
            sweetify.error(
                request, 'Porfavor cadastre seus dados antes de fazer um pedido')
            return redirect('perfil')
        pedidos = Pedido.objects.filter(revendedor=request.user.revendedor).exclude(
            completo=False).order_by('-data')
    elif request.user.tipo == User.LOJA:
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
    if request.user.tipo == User.REVENDEDOR:
        pedido = Pedido.objects.get(id=pk)
        try:
            pedido_ex = Pedido.objects.get(
                revendedor=request.user.revendedor, completo=False)
        except:
            pedido_ex = False
        if pedido_ex:
            pedido_ex.delete()
        pedido.completo = False
        pedido.devolve_produtos()
        pedido.save()
        sweetify.info(
            request, 'Por favor altere o pedido a faça checkout novamente')
        return redirect('produtos')
    elif request.user.tipo == User.LOJA:
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
        pedido = Pedido.objects.get(id=pk)
        if request.user.tipo == User.FRANQUIA or request.user.tipo == User.SUPERVISOR:
            if pedido.revendedor:
                request.session['revendped_id'] = pedido.revendedor.id
                request.session['tipo'] = 'revendedor'
                pedido.completo = False
                pedido.devolve_produtos()
                pedido.save()
                sweetify.info(
                    request, 'Por favor altere o pedido a faça checkout novamente')
                return redirect('produtos')
            else:
                request.session['revendped_id'] = pedido.loja.id
                request.session['tipo'] = 'loja'
                pedido.completo = False
                pedido.devolve_produtos()
                pedido.save()
                sweetify.info(
                    request, 'Por favor altere o pedido a faça checkout novamente')
                return redirect('produtos')
        else:
            if pedido.revendedor:
                pedido_ex = Pedido.objects.get(
                    revendedor=pedido.revendedor, completo=False)
                request.session['revendped_id'] = pedido.revendedor.id
                request.session['tipo'] = 'revendedor'
                pedido_ex.delete()
                pedido.completo = False
                pedido.devolve_produtos()
                pedido.save()
                sweetify.info(
                    request, 'Por favor altere o pedido a faça checkout novamente')
                return redirect('produtos')
            else:
                pedido_ex = Pedido.objects.get(
                    loja=pedido.loja, completo=False)
                request.session['revendped_id'] = pedido.loja.id
                request.session['tipo'] = 'loja'
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
    pedido.status = Pedido.CANCELADO
    pedido.save()
    sweetify.success(request, 'Pedido cancelado com sucesso')
    if request.user.tipo not in (User.SUPERVISOR, User.FRANQUIA):
        return redirect('meus_pedidos')
    else:
        return redirect('pedidos')


@login_required
@user_passes_test(supervisor_franquia_check)
def lista_usuarios(request):
    usuarios = User.objects.all().order_by('-criado')
    if aprovado_check(request.user):
        return render(request, "vendas/usuarios.html", {'usuarios': usuarios})
    else:
        sweetify.info(request, 'por favor aguarde o cadastro ser aprovado')
        return redirect('vendas-home')


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
    pedidos = Pedido.objects.all().exclude(completo=False).order_by('-data')
    if aprovado_check(request.user):
        return render(request, "vendas/pedidos.html", {'pedidos': pedidos})
    else:
        sweetify.info(request, 'por favor aguarde o cadastro ser aprovado')
        return redirect('vendas-home')


@login_required
@user_passes_test(franquia_check)
def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, "vendas/cadastro_produtos.html", {'produtos': produtos})


@login_required
@user_passes_test(supervisor_franquia_check)
def atualizarProduto(request, pk):
    produto = Produto.objects.get(id=pk)

    if request.method == 'POST':
        form = FormProduto(request.POST, request.FILES, instance=produto)
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
        form = FormProduto(request.POST, request.FILES)
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
    pedido.status = Pedido.APROVADO
    pedido.save()
    sweetify.success(request, 'Pedido aprovado!')
    return redirect('pedidos')


@login_required
@user_passes_test(franquia_check)
def enviarPedido(request, pk):
    pedido = Pedido.objects.get(id=pk)
    pedido.status = Pedido.ENVIADO
    pedido.save()
    sweetify.success(request, 'Pedido enviado!')
    return redirect('pedidos')


@login_required
def confirmarPedido(request, pk):
    pedido = Pedido.objects.get(id=pk)
    pedido.status = Pedido.FINALIZADO
    pedido.save()
    sweetify.success(request, 'Pedido finalizado!')
    return redirect('meus_pedidos')


class pesquisaUsuarios(LoginRequiredMixin, ListView):
    model = User

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = User.objects.filter(
            Q(email__icontains=query) | Q(tipo__icontains=query)
        ).order_by('-criado')
        return object_list


def pesquisaRevNovo(request):
    from itertools import chain
    if request.user.tipo == User.FRANQUIA:
        revendedor_list = Revendedor.objects.filter(is_aprovado=False)
        loja_list = Loja.objects.filter(is_aprovado=False)
        supervisor_list = Supervisor.objects.filter(is_aprovado=False)
        object_list = list(chain(revendedor_list, loja_list, supervisor_list))
        print(object_list)
    else:
        object_list = Revendedor.objects.filter(is_aprovado=False)

    return render(request, 'vendas/revendedor_list.html', {'object_list': object_list})


class pesquisaPedidos(LoginRequiredMixin, ListView):
    model = Pedido

    def get_queryset(self):
        query = self.request.GET.get("q")
        if self.request.user.tipo == User.REVENDEDOR:
            object_list = Pedido.objects.filter(Q(completo=True), Q(revendedor=self.request.user.revendedor),
                                                Q(cod_pedido__icontains=query) | Q(
                                                    status__icontains=query)
                                                | Q(metodo_de_pagamento__icontains=query)
                                                )
        elif self.request.user.tipo == User.LOJA:
            object_list = Pedido.objects.filter(Q(completo=True), Q(loja=self.request.user.loja),
                                                Q(cod_pedido__icontains=query) | Q(
                                                    status__icontains=query)
                                                | Q(metodo_de_pagamento__icontains=query)
                                                )
        else:
            object_list = Pedido.objects.filter(Q(completo=True),
                                                Q(cod_pedido__icontains=query) | Q(
                                                    status__icontains=query)
                                                | Q(metodo_de_pagamento__icontains=query)
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
    iniciante, bronze, prata, ouro, diamante = Meta.objects.all()
    print(Meta.objects.all())

    for revendedor in revendedores:
        if revendedor.total_comprado_mes >= diamante.valor:
            revendedor.meta = diamante
        elif revendedor.total_comprado_mes >= ouro.valor:
            revendedor.meta = ouro
        elif revendedor.total_comprado_mes >= prata.valor:
            revendedor.meta = prata
        elif revendedor.total_comprado_mes >= bronze.valor:
            revendedor.meta = bronze
        elif revendedor.total_comprado_mes < bronze.valor:
            revendedor.meta = iniciante
        revendedor.save()

    sweetify.success(request, 'Metas atualizadas com sucesso')
    return redirect('metas')


def atualizarRelatorio(request):
    dados = json.loads(request.body)

    request.session['data'] = dados['data']
    request.session['grupo'] = dados['grupo']

    return JsonResponse('feito', safe=False)


def relatorios(request):
    now = datetime.datetime.now()
    data_filtro = request.session.get('data')
    grupo = request.session.get('grupo')

    if data_filtro == None:
        data_filtro = 'month'
    if grupo == None:
        grupo = 'ambos'

    key = getattr(now, data_filtro)
    filtro = 'data__' + data_filtro
    filtro_user = 'criado__' + data_filtro

    if data_filtro == 'month':
        data = format_date(now, "MMMM", locale='pt_BR').capitalize()
    elif data_filtro == 'day':
        data = format_date(now, "EEEE", locale='pt_BR').capitalize()
    elif data_filtro == 'year':
        data = now.strftime("%Y")

    soma = 0
    if grupo == 'lojas':
        pedidos_cancel = request.user.franquia.pedido_set.filter(
            revendedor=None, **{filtro: key})
        pedidos = pedidos_cancel.exclude(status=Pedido.CANCELADO)
    elif grupo == 'revendedores':
        pedidos_cancel = request.user.franquia.pedido_set.filter(
            loja=None, **{filtro: key})
        pedidos = pedidos_cancel.exclude(status=Pedido.CANCELADO)
    else:
        pedidos_cancel = request.user.franquia.pedido_set.filter(
            **{filtro: key})
        pedidos = pedidos_cancel.exclude(status=Pedido.CANCELADO)

    users_rev = User.objects.filter(
        tipo=User.REVENDEDOR, **{filtro_user: key}).count()

    qtde_pedidos = pedidos_cancel.filter().count()
    qtde_pedidos_pendentes = pedidos.filter(status=Pedido.APROV_PEND).count()
    qtde_pedidos_aprovados = pedidos.filter(status=Pedido.APROVADO).count()
    qtde_pedidos_enviados = pedidos.filter(status=Pedido.ENVIADO).count()
    qtde_pedidos_finalizados = pedidos.filter(status=Pedido.FINALIZADO).count()
    qtde_pedidos_cancelados = pedidos_cancel.filter(
        status=Pedido.CANCELADO).count()

    total = sum([pedido.get_meta_total for pedido in pedidos])
    subtotal = sum([pedido.get_carrinho_total for pedido in pedidos])

    context = {
        'data': data,
        'total': total,
        'subtotal': subtotal,
        'data_filtro': data_filtro,
        'grupo': grupo,
        'revendedores': soma,
        'qtde_pedidos': qtde_pedidos,
        'qtde_pedidos_pendentes': qtde_pedidos_pendentes,
        'qtde_pedidos_aprovados': qtde_pedidos_aprovados,
        'qtde_pedidos_enviados': qtde_pedidos_enviados,
        'qtde_pedidos_finalizados': qtde_pedidos_finalizados,
        'qtde_pedidos_cancelados': qtde_pedidos_cancelados,
        'novos_revendedores': users_rev,
    }

    return render(request, 'vendas/relatorios.html', context)


def graficoProdutos(request):
    import itertools

    now = datetime.datetime.now()
    data_filtro = request.session.get('data')
    if data_filtro == None:
        data_filtro = 'month'

    key = getattr(now, data_filtro)
    filtro = 'data__' + data_filtro

    dados = []
    item = []
    response = {}

    pedidos_cancel = Pedido.objects.filter(
        completo=True, **{filtro: key})
    pedidos = pedidos_cancel.exclude(status=Pedido.CANCELADO)
    for pedido in pedidos:
        set = pedido.itempedido_set.all()
        for i in set:
            item.append(i)

    for j in item:
        dados.append({j.produto.nome: j.quantidade})

    for d in dados:
        key = list(d.keys())[0]
        response[key] = response.get(key, 0) + d[key]

    sorted_response = dict(
        sorted(response.items(), key=lambda item: item[1], reverse=True))

    sorted_response = dict(itertools.islice(sorted_response.items(), 10))

    return JsonResponse(sorted_response, safe=False)


def graficoRevendedores(request):
    import itertools

    now = datetime.datetime.now()
    data_filtro = request.session.get('data')

    if data_filtro == None:
        data_filtro = 'month'

    key = getattr(now, data_filtro)
    filtro = 'data__' + data_filtro

    dados = []
    response = {}

    pedidos = request.user.franquia.pedido_set.filter(completo=True,
                                                      loja=None, **{filtro: key}).exclude(status=Pedido.CANCELADO)
    for pedido in pedidos:
        dados.append({pedido.revendedor.nome: pedido.get_meta_total})

    for d in dados:
        key = list(d.keys())[0]
        response[key] = response.get(key, 0) + d[key]

    print(response)

    sorted_response = dict(
        sorted(response.items(), key=lambda item: item[1], reverse=True))

    sorted_response = dict(itertools.islice(sorted_response.items(), 10))

    return JsonResponse(sorted_response, safe=False)


def graficoLojas(request):
    import itertools

    now = datetime.datetime.now()
    data_filtro = request.session.get('data')
    if data_filtro == None:
        data_filtro = 'month'
    key = getattr(now, data_filtro)
    filtro = 'data__' + data_filtro

    dados = []
    response = {}

    pedidos = request.user.franquia.pedido_set.filter(completo=True,
                                                      revendedor=None, **{filtro: key}).exclude(status=Pedido.CANCELADO)
    print(pedidos)
    for pedido in pedidos:
        dados.append({pedido.loja.nome_fantasia: pedido.get_meta_total})

    for d in dados:
        key = list(d.keys())[0]
        response[key] = response.get(key, 0) + d[key]

    sorted_response = dict(
        sorted(response.items(), key=lambda item: item[1], reverse=True))

    sorted_response = dict(itertools.islice(sorted_response.items(), 10))

    return JsonResponse(sorted_response, safe=False)


def graficoTempo(request):

    now = datetime.datetime.now()
    data_filtro = request.session.get('data')
    if data_filtro == None:
        data_filtro = 'month'
    key = getattr(now, data_filtro)
    filtro = 'data__' + data_filtro

    dados = []
    response = {}

    pedidos = Pedido.objects.filter(
        completo=True, **{filtro: key}).exclude(status=Pedido.CANCELADO)

    if data_filtro == 'day':
        for pedido in pedidos:
            dados.append({str(pedido.data.hour): 1})
    if data_filtro == 'month':
        for pedido in pedidos:
            dados.append({str(pedido.data.day): 1})
    if data_filtro == 'year':
        for pedido in pedidos:
            dados.append({str(pedido.data.month): 1})

    for d in dados:
        key = list(d.keys())[0]
        response[key] = response.get(key, 0) + d[key]

    return JsonResponse(response, safe=False)
