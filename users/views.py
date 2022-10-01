from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import PerfilRevendedor, UserRegisterForm
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def perfil_revendedor(request):
    if request.method == 'POST':
        form = PerfilRevendedor(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = PerfilRevendedor()
    return render(request, 'users/perfil_revendedor.html', {'form': form})

    # request.user, 
