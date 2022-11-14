from django.urls import path
from . import views
from .views import (
    pesquisaProdutos,
    pesquisaUsuarios,
    pesquisaPedidos,
)

urlpatterns = [
    path('', views.home, name='vendas-home'),
    path('perfil/', views.perfil, name='perfil'),

    path('meus_pedidos/', views.mostrarPedidos, name='meus_pedidos'),
    path('detalhe_pedido/<int:pk>/', views.detalhePedido, name='detalhe_pedido'),
    path('atualizar_pedido/<int:pk>/',views.atualizarPedido, name='atualizar_pedido'),
    path('deletar_pedido/<int:pk>/', views.deletarPedido, name='deletar_pedido'),
    path('aprovar_pedido/<int:pk>/', views.aprovarPedido, name='aprovar_pedido'),
    path('enviar_pedido/<int:pk>/', views.enviarPedido, name='enviar_pedido'),
    path('confirmar_pedido/<int:pk>/',views.confirmarPedido, name='confirmar_pedido'),

    path('produtos/', views.produtos, name="produtos"),
    path('carrinho/', views.carrinho, name="carrinho"),
    path('checkout/', views.checkout, name="checkout"),

    path('atualizar_item/', views.atualizarItem, name="atualizar_item"),
    path('processarPedido/', views.processarPedido, name="processarPedido"),

    path('usuarios/', views.lista_usuarios, name='usuarios'),
    path('atualizar_usuario/<int:pk>/',
         views.atualizarUsuario, name='atualizar_usuario'),
    path('deletar_usuario/<int:pk>/',
         views.deletarUsuario, name='deletar_usuario'),

    path('pedidos/', views.lista_pedidos, name='pedidos'),
    path('deletar_pedido/<int:pk>/', views.deletarPedido, name='deletar_pedido'),

    path('cadastro_produtos/', views.lista_produtos, name='cadastro_produtos'),
    path('adicionar_produto/', views.adicionarProduto, name='adicionar_produto'),
    path('atualizar_produto/<int:pk>/',
         views.atualizarProduto, name='atualizar_produto'),
    path('deletar_produto/<int:pk>/',
         views.deletarProduto, name='deletar_produto'),

    path('pesquisa_usuarios/', pesquisaUsuarios.as_view(),
         name='pesquisa_usuarios'),
    path('pesquisa_pedidos/', pesquisaPedidos.as_view(), name='pesquisa_pedidos'),
    path('pesquisa_produtos/', pesquisaProdutos.as_view(),
         name='pesquisa_produtos'),

    path('metas/', views.metas, name='metas'),
    path('atualizar_meta/<int:pk>/', views.atualizarMeta, name='atualizar_meta'),
    path('atualizar_metas_revendedores/', views.atualizarMetasRevendedores,
         name='atualizar_metas_revendedores'),

    path('atualizar_relatorio/', views.atualizarRelatorio,
         name='atualizar_relatorio'),
    path('relatorios/', views.relatorios, name='relatorios'),
    path('grafico_produtos/', views.graficoProdutos, name='grafico_produtos'),
    path('grafico_revendedores/', views.graficoRevendedores, name='grafico_revendedores'),
    path('grafico_lojas/', views.graficoLojas, name='grafico_lojas'),

]
