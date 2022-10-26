from django.contrib import admin
from .models import Franquia, ItemPedido, Produto, Revendedor, Pedido, Supervisor

admin.site.register(Revendedor)
admin.site.register(Produto)
admin.site.register(Pedido)
admin.site.register(ItemPedido)
admin.site.register(Supervisor)
admin.site.register(Franquia)
