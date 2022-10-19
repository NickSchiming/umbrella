from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import sweetify
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from vendas.models import Pedido, Revendedor
from .forms import *
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


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


def fazer_pedido(request):
    PedidoFormSet = inlineformset_factory(
        User, Pedido, fields=('produto',), extra=3)
    formset = PedidoFormSet(
        queryset=Pedido.objects.none(), instance=request.user)

    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        form = FormPedido(request.POST)
        formset = PedidoFormSet(request.POST, instance=request.user)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'form': formset}
    return render(request, 'vendas/pedido_form.html', context)
