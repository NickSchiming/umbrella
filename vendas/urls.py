from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='vendas-home'),
    path('perfil/', views.perfil, name='perfil'),
    
    path('meus_pedidos/', views.mostrarPedidos, name='meus_pedidos'),
    path('detalhe_pedido/<int:pk>/', views.detalhePedido, name='detalhe_pedido'),
    path('atualizar_pedido/<int:pk>/', views.atualizarPedido, name='atualizar_pedido'),
    path('deletar_pedido/<int:pk>/', views.deletarPedido, name='deletar_pedido'),

    path('produtos/', views.produtos, name="produtos"),
    path('carrinho/', views.carrinho, name="carrinho"),
    path('checkout/', views.checkout, name="checkout"),

    path('atualizar_item/', views.atualizarItem, name="atualizar_item"),
    path('processarPedido/', views.processarPedido, name="processarPedido"),

    path('usuarios/', views.lista_usuarios, name='usuarios'),
    path('atualizar_usuario/<int:pk>/', views.atualizarUsuario, name='atualizar_usuario'),
    path('deletar_usuario/<int:pk>/', views.deletarUsuario, name='deletar_usuario'),

    path('pedidos/', views.lista_pedidos, name='pedidos'),
    path('deletar_pedido/<int:pk>/', views.deletarPedido, name='deletar_pedido'),

    path('cadastro_produtos/', views.lista_produtos, name='cadastro_produtos'),
    path('atualizar_produto/<int:pk>/', views.atualizarProduto, name='atualizar_produto'),
    path('deletar_produto/<int:pk>/', views.deletarProduto, name='deletar_produto'),
]
