from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='vendas-home'),
    path('perfil/', views.perfil, name='perfil'),
    
    path('produtos/', views.produtos, name="produtos"),
    path('carrinho/', views.carrinho, name="carrinho"),
    path('checkout/', views.checkout, name="checkout"),
    
    path('atualizar_item/', views.atualizarItem, name="atualizar_item"),
	# path('process_order/', views.processOrder, name="process_order"),
]