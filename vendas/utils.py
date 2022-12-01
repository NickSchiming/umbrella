import sweetify
from django.shortcuts import render, redirect

from vendas.forms import PerfilFranquia, PerfilLoja, PerfilRevendedor, PerfilSupervisor, UserUpdateForm
from .models import *
import logging

logger = logging.getLogger(__name__)


def dadosCarrinho(request, revendedorPed):
    if request.user.tipo == User.REVENDEDOR:
        revendedor = request.user.revendedor
        pedido, criado = Pedido.objects.get_or_create(
            revendedor=revendedor, completo=False)
        itens = pedido.itempedido_set.all()
        itensCarrinho = pedido.get_carrinho_itens
        return {'itensCarrinho': itensCarrinho, 'pedido': pedido, 'itens': itens}
    elif request.user.tipo == User.LOJA:
        loja = request.user.loja
        pedido, criado = Pedido.objects.get_or_create(
            loja=loja, completo=False)
        itens = pedido.itempedido_set.all()
        itensCarrinho = pedido.get_carrinho_itens
        return {'itensCarrinho': itensCarrinho, 'pedido': pedido, 'itens': itens}
    else:
        revendedor = revendedorPed
        try:
            pedido, criado = Pedido.objects.get_or_create(
                revendedor=revendedor, completo=False)
        except:
            pedido, criado = Pedido.objects.get_or_create(
                loja=revendedor, completo=False)
        itens = pedido.itempedido_set.all()
        itensCarrinho = pedido.get_carrinho_itens
        return {'itensCarrinho': itensCarrinho, 'pedido': pedido, 'itens': itens}


def renderForm(request, user):

    reload = False

    if user.tipo == User.REVENDEDOR:
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=user)
            try:
                p_form = PerfilRevendedor(
                    request.POST, instance=user.revendedor)
            except:
                p_form = PerfilRevendedor(request.POST)

            reload = salvaForm(request, user, p_form, u_form)

        else:
            u_form = UserUpdateForm(instance=user)
            try:
                p_form = PerfilRevendedor(instance=user.revendedor)
            except:
                p_form = PerfilRevendedor()

    elif user.tipo == User.FRANQUIA:
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=user)
            try:
                p_form = PerfilFranquia(
                    request.POST, instance=user.franquia)
            except:
                p_form = PerfilFranquia(request.POST)

            reload = salvaForm(request, user, p_form, u_form)

        else:
            u_form = UserUpdateForm(instance=user)
            try:
                p_form = PerfilFranquia(instance=user.franquia)
            except:
                p_form = PerfilFranquia()

    elif user.tipo == User.LOJA:
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=user)
            try:
                p_form = PerfilLoja(
                    request.POST, instance=user.loja)
            except:
                p_form = PerfilLoja(request.POST)

            reload = salvaForm(request, user, p_form, u_form)

        else:
            u_form = UserUpdateForm(instance=user)
            try:
                p_form = PerfilLoja(instance=user.loja)
            except:
                p_form = PerfilLoja()

    elif user.tipo == User.SUPERVISOR:
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=user)
            try:
                p_form = PerfilSupervisor(
                    request.POST, instance=user.supervisor)
            except:
                p_form = PerfilSupervisor(request.POST)

            reload = salvaForm(request, user, p_form, u_form)
        else:
            u_form = UserUpdateForm(instance=user)
            try:
                p_form = PerfilSupervisor(instance=user.supervisor)
            except:
                p_form = PerfilSupervisor()

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user': user,
        'reload': reload
    }

    return context


def salvaForm(request, user, p_form, u_form):
    if p_form.has_changed():
        if u_form.is_valid() and p_form.is_valid():
            if temNone(p_form):
                sweetify.error(
                    request, 'Preencha todos os campos para continuar')
            else:
                u_form.save()
                form = p_form.save(commit=False)
                form.user = user
                p_form.save()
                sweetify.success(request, 'Seus dados foram atualizados')
        else:
            sweetify.error(
                request, 'Houve um erro na atualização dos dados')
    else:
        if u_form.is_valid():
            u_form.save()
            sweetify.success(request, 'Seus dados foram atualizados')

    if request.user.tipo == User.SUPERVISOR and user.tipo == User.REVENDEDOR:
        try:
            user.revendedor.supervisor = request.user.supervisor
            user.revendedor.save()
        except:
            pass

    if request.user.tipo == User.FRANQUIA and user.tipo == User.SUPERVISOR:
        try:
            user.supervisor.franquia = request.user.franquia
            user.supervisor.save()
        except:
            pass

    if request.user.tipo == User.FRANQUIA and user.tipo == User.LOJA:
        try:
            user.loja.franquia = request.user.franquia
            user.loja.save()
        except:
            pass

    return True


def temNone(p_form):
    x = False
    for field in p_form:
        if field.value() == None or field.value() == '':
            x = True

    return x


def infoHome(user, pedidos):

    try:
        total = sum([pedido.get_meta_total for pedido in pedidos])
        subtotal = sum([pedido.get_carrinho_total for pedido in pedidos])
        qtde_pedidos_pendentes = pedidos.filter(
            completo=True, status=Pedido.APROV_PEND).count()
        qtde_pedidos_aprovados = pedidos.filter(status=Pedido.APROVADO).count()
        qtde_pedidos_cancelados = pedidos.filter(
            status=Pedido.CANCELADO).count()
        qtde_pedidos_enviados = pedidos.filter(status=Pedido.ENVIADO).count()
        qtde_pedidos_finalizados = pedidos.filter(
            status=Pedido.FINALIZADO).count()
    except:
        total = 0
        subtotal = 0

        qtde_pedidos_pendentes = 0
        qtde_pedidos_aprovados = 0
        qtde_pedidos_enviados = 0
        qtde_pedidos_finalizados = 0

    context = {
        'user': user,
        'total': total,
        'subtotal': subtotal,
        'qtde_pedidos_pendentes': qtde_pedidos_pendentes,
        'qtde_pedidos_aprovados': qtde_pedidos_aprovados,
        'qtde_pedidos_enviados': qtde_pedidos_enviados,
        'qtde_pedidos_finalizados': qtde_pedidos_finalizados,
        'qtde_pedidos_cancelados': qtde_pedidos_cancelados
    }
    return context


def perfil_u_form_post(request):
    u_form = UserUpdateForm(request.POST, instance=request.user)
    if not request.user.tipo == User.FRANQUIA:
        u_form.fields.pop('tipo')

    return u_form


def perfil_u_form_get(request):
    u_form = UserUpdateForm(instance=request.user)
    if not request.user.tipo == User.FRANQUIA:
        u_form.fields.pop('tipo')
    return u_form


def tira_field_perfil_rev(request, tipo, p_form):
    if not request.user.tipo == User.FRANQUIA:
        if tipo == User.LOJA or tipo == User.SUPERVISOR:
            try:
                p_form.fields.pop('is_aprovado')
            except:
                pass
    if tipo == User.REVENDEDOR:
        if not request.user.tipo == User.FRANQUIA or not request.user.tipo == User.SUPERVISOR:
            try:
                p_form.fields.pop('is_aprovado')
                p_form.fields.pop('meta')
            except:
                pass


def salva_p_form(request, tipo, u_form, p_form):
    if tipo == User.REVENDEDOR:
        if not tipo == User.FRANQUIA or not tipo == User.SUPERVISOR:
            p_form.fields.pop('is_aprovado')
            p_form.fields.pop('meta')

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
    else:
        sweetify.error(request, 'Houve um erro na atualização dos dados')


def aprovado_check(user):
    if hasattr(user, 'supervisor'):
        if user.supervisor.is_aprovado:
            return True
        else:
            return False
    elif hasattr(user, 'franquia'):
        if user.franquia.is_aprovado:
            return True
        else:
            return False
    elif hasattr(user, 'loja'):
        if user.loja.is_aprovado:
            return True
        else:
            return False
    elif hasattr(user, 'revendedor'):
        if user.revendedor.is_aprovado:
            return True
        else:
            return False
