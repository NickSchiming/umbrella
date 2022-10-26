from django.urls import path
from . import views
from .views import detalhePedido

urlpatterns = [
    path('', views.home, name='vendas-home'),
    path('perfil/', views.perfil, name='perfil'),
    
    path('meus_pedidos/', views.mostrarPedidos, name='meus_pedidos'),
    path('detalhe_pedido/<int:pk>/', detalhePedido.as_view(), name='detalhe_pedido'),

    path('produtos/', views.produtos, name="produtos"),
    path('carrinho/', views.carrinho, name="carrinho"),
    path('checkout/', views.checkout, name="checkout"),

    path('atualizar_item/', views.atualizarItem, name="atualizar_item"),
    path('processarPedido/', views.processarPedido, name="processarPedido"),
]
