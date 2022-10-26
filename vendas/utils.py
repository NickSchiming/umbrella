import datetime
import json
from .models import *
import logging

logger = logging.getLogger(__name__)

def dadosCarrinho(request):
    if request.user.is_authenticated:
        revendedor = request.user.revendedor
        pedido, criado = Pedido.objects.get_or_create(revendedor=revendedor, completo=False)
        itens = pedido.itempedido_set.all()
        itensCarrinho = pedido.get_carrinho_itens

    return {'itensCarrinho':itensCarrinho, 'pedido': pedido, 'itens':itens}
