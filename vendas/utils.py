import sweetify
from django.shortcuts import render, redirect

from vendas.forms import PerfilFranquia, PerfilRevendedor, UserUpdateForm
from .models import *
import logging

logger = logging.getLogger(__name__)

def dadosCarrinho(request):
    if request.user.is_authenticated:
        revendedor = request.user.revendedor
        pedido, criado = Pedido.objects.get_or_create(revendedor=revendedor, completo=False)
        itens = pedido.itempedido_set.all()
        itensCarrinho = pedido.get_carrinho_itens

    return {'itensCarrinho':itensCarrinho, 'pedido': pedido, 'itens':itens}


def renderForm(request, user):

        if user.type == 'REVENDEDOR':
            if request.method == 'POST':
                u_form = UserUpdateForm(request.POST, instance=user)
                try:
                    p_form = PerfilRevendedor(
                    request.POST, instance=user.revendedor)
                except:
                    p_form = PerfilRevendedor(request.POST)
                if u_form.is_valid() and p_form.is_valid():
                    u_form.save()
                    form = p_form.save(commit=False)
                    form.user = user                    
                    p_form.save()

                    sweetify.success(request, 'Seus dados foram atualizados')
                else:
                    sweetify.error(request, 'Houve um erro na atualização dos dados')

            else:
                u_form = UserUpdateForm(instance=user)
                try:
                    p_form = PerfilRevendedor(instance=user.revendedor)
                except:
                    p_form = PerfilRevendedor()

            return {
            'u_form': u_form,
            'p_form': p_form
            }
        elif user.type == 'FRANQUIA':
            if request.method == 'POST':
                u_form = UserUpdateForm(request.POST, instance=user)
                try:
                    p_form = PerfilFranquia(
                    request.POST, instance=user.franquia)
                except:
                    p_form = PerfilFranquia(request.POST)
                if u_form.is_valid() and p_form.is_valid():
                    u_form.save()
                    form = p_form.save(commit=False)
                    logger.warning(user)
                    form.user = user
                    logger.warning(form.user)
                    logger.warning(p_form.save())
                    p_form.save()

                    sweetify.success(request, 'Seus dados foram atualizados')
                else:
                    sweetify.error(request, 'Houve um erro na atualização dos dados')

            else:
                u_form = UserUpdateForm(instance=user)
                try:
                    p_form = PerfilFranquia(instance=user.franquia)
                except:
                    p_form = PerfilFranquia()

            return {
            'u_form': u_form,
            'p_form': p_form
            }