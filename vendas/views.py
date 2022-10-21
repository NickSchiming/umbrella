from sqlite3 import DatabaseError
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import sweetify

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


def fazer_pedido(request):
    ItemPedidoFormSet = inlineformset_factory(
       Pedido, Item_pedido,  fields=('produto', 'quantidade'), extra=1)

    pedido = Pedido.objects.get()
    
    if request.method == 'GET':
         formset = ItemPedidoFormSet(request.GET or None)
    elif request.method == 'POST':
        formset = ItemPedidoFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    try:
                        if form.cleaned_data.get('DELETE') and form.instance.pk:
                            form.instance.delete()
                        else:
                            instance = form.save(commit=False)
                            instance.pedido = request.pedido
                            instance.save()
                            sweetify.success(request, "Payments saved successfully")
                    except DatabaseError:
                        sweetify.error(request, "Database error. Please try again")
            return redirect('/')
    # else:
    #     formset = ItemPedidoFormSet(
    #         queryset=Pedido.objects.none())

    context = {'formset': formset}
    return render(request, 'vendas/pedido_form.html', context)
