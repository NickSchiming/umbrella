from django.urls import path
from . import views
from vendas import views as vendas_views

urlpatterns = [
    path('', views.home, name='vendas-home'),
    path('perfil/', vendas_views.perfil, name='perfil'),
    
    path('fazer_pedido/', vendas_views.fazer_pedido, name="fazer_pedido"),
    path('listar_pedidos/', vendas_views.listar_pedidos.as_view(), name="listar_pedidos"),
]