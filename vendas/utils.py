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
        try:
            user.supervisor.franquia = request.user.franquia
            user.supervisor.save()
        except:
            pass

    return True


def temNone(p_form):
    x = False
    for field in p_form:
        if field.value() == None or field.value() == '':
            x = True

    return x


def formPerfil(request, tipo):
    ldict = {'request': request}
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if not request.user.type == 'FRANQUIA':
            u_form.fields.pop('type')
        try:
            exec('p_form = Perfil' + tipo + '(request.POST, instance=request.user.' + tipo.lower() + ')',globals(),ldict)
        except:
            exec('p_form = Perfil' + tipo + '(request.POST)',globals(),ldict)
        
        p_form = ldict['p_form']

        if tipo == 'Revendedor':
            if not request.user.type == 'FRANQUIA' or not request.user.type == 'SUPERVISOR':
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
                try:
                    if form.meta == None:
                        form.meta = Meta.objects.get(nivel=Meta.INICIANTE)
                except:
                    pass
                p_form.save()
                sweetify.success(request, 'Seus dados foram atualizados')
        else:
            sweetify.error(
                request, 'Houve um erro na atualização dos dados')

    else:


        u_form = UserUpdateForm(instance=request.user)
        if not request.user.type == 'FRANQUIA':
            u_form.fields.pop('type')
        try:
            exec('p_form = Perfil' + tipo + '(instance=request.user.' + tipo.lower() + ')',globals(),ldict)
        except:
            exec('p_form = Perfil' + tipo + '()',globals(),ldict)
            
        p_form = ldict['p_form']

        if tipo == 'Revendedor':
            if not request.user.type == 'FRANQUIA' or not request.user.type == 'SUPERVISOR':
                p_form.fields.pop('is_aprovado')
                p_form.fields.pop('meta')

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return context
    

# def infoHome(request):
#     pedidos = user.revendedor.pedido_set.filter(completo = True,
#             data__month=now.month)
#     width = str((user.revendedor.total_comprado /
#                 user.revendedor.get_proxima_meta.valor) * 100) + '%'

#     total = sum([pedido.get_meta_total for pedido in pedidos])
#     subtotal = sum([pedido.get_carrinho_total for pedido in pedidos])
#     qtde_pedidos_pendentes = pedidos.filter(completo=True, status=Pedido.APROV_PEND).count()
#     qtde_pedidos_aprovados = pedidos.filter(status=Pedido.APROVADO).count()
#     qtde_pedidos_enviados = pedidos.filter(status=Pedido.ENVIADO).count()
#     qtde_pedidos_finalizados = pedidos.filter(status=Pedido.FINALIZADO).count()

#     context = {
#         'user': user,
#         'width': width,
#         'total': total,
#         'subtotal': subtotal,
#         'qtde_pedidos_pendentes': qtde_pedidos_pendentes,
#         'qtde_pedidos_aprovados': qtde_pedidos_aprovados,
#         'qtde_pedidos_enviados': qtde_pedidos_enviados,
#         'qtde_pedidos_finalizados': qtde_pedidos_finalizados,

#     }