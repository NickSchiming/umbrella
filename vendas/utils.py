import sweetify
from django.shortcuts import render, redirect

from vendas.forms import PerfilFranquia, PerfilLoja, PerfilRevendedor, PerfilSupervisor, UserUpdateForm
from .models import *
import logging

logger = logging.getLogger(__name__)


def dadosCarrinho(request, revendedorPed):
    if request.user.type == "REVENDEDOR":
        revendedor = request.user.revendedor
        pedido, criado = Pedido.objects.get_or_create(
            revendedor=revendedor, completo=False)
        itens = pedido.itempedido_set.all()
        itensCarrinho = pedido.get_carrinho_itens
        return {'itensCarrinho': itensCarrinho, 'pedido': pedido, 'itens': itens}
    elif request.user.type == "LOJA":
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
        revendedorPed = None
        return {'itensCarrinho': itensCarrinho, 'pedido': pedido, 'itens': itens}


def renderForm(request, user):

    reload = False

    if user.type == 'REVENDEDOR':
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

    elif user.type == 'FRANQUIA':
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

    elif user.type == 'LOJA':
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

    elif user.type == 'SUPERVISOR':
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

    if request.user.type == 'SUPERVISOR' and user.type == 'REVENDEDOR':
        user.revendedor.supervisor = request.user.supervisor
        user.revendedor.save()
    
    if request.user.type == 'FRANQUIA' and user.type == 'SUPERVISOR':
        user.supervisor.franquia = request.user.franquia
        user.supervisor.save()

    return True


def temNone(p_form):
    x = False
    for field in p_form:
        if field.value() == None or field.value() == '':
            x = True

    return x
