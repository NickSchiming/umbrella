from django.shortcuts import render, redirect
from .forms import  UserRegisterForm
import sweetify


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            sweetify.success(request, 'Conta criada com sucesso! Agora voce pode fazer login')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})