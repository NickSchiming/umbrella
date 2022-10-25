import json
from .models import *
import logging

def cookieCarrinho(request):

	#Create empty cart for now for non-logged in user
	try:
		carrinho = json.loads(request.COOKIES['carrinho'])
	except:
		carrinho = {}
		print('CARRINHO:', carrinho)

	itens = []
	order = {'get_carrinho_total':0, 'get_carrinho_itens':0}
	itens_carrinho = order['get_carrinho_itens']

	for i in carrinho:
		#We use try block to prevent items in cart that may have been removed from causing error
		try:	
			if(carrinho[i]['quantidade']>0): #items with negative quantity = lot of freebies  
				itens_carrinho += carrinho[i]['quantidade']

				produto = Produto.objects.get(id=i)
				total = (produto.price * carrinho[i]['quantidade'])

				order['get_cart_total'] += total
				order['get_cart_items'] += carrinho[i]['quantidade']

				item = {
				'id':produto.id,
				'produto':{'id':produto.id,'nome':produto.nome, 'preco':produto.preco, 
				}, 'quantidade':carrinho[i]['quantidade'],
				'get_total':total,
				}
				itens.append(item)
		except:
			pass
			
	return {'itens_carrinho':itens_carrinho ,'order':order, 'itens':itens}

def dadosCarrinho(request):
    if request.user.is_authenticated:
        revendedor = request.user
        pedido, criado = Pedido.objects.get_or_create(revendedor=revendedor)
        itens = pedido.itempedido_set.all()
        itensCarrinho = pedido.get_carrinho_itens
    else:
        dadosCookie = cookieCarrinho(request)
        itensCarrinho = dadosCookie['cartItems']
        pedido = dadosCookie['order']
        itens = dadosCookie['itens']

    return {'itensCarrinho':itensCarrinho ,'pedido':pedido, 'itens':itens}

	
# def pedidoConvidado(request, dados):
# 	nome = dados['form']['nome']
# 	email = dados['form']['email']

# 	dadosCookie = cookieCarrinho(request)
# 	itens = dadosCookie['itens']

# 	revendedor, created = Revendedor.objects.get_or_create(
# 			email=email,
# 			)
# 	revendedor.name = nome
# 	revendedor.save()

# 	pedido = Pedido.objects.create(revendedor=revendedor)

# 	for item in itens:
# 		produto = Produto.objects.get(id=item['id'])
# 		itemPedido = ItemPedido.objects.create(
# 			produto=produto,
# 			pedido=pedido,
# 			quantidade=(item['quantidade'] if item['quantidade']>0 else -1*item['quantidade']), # negative quantity = freebies
# 		)
# 	return revendedor, pedido