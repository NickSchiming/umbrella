from django.contrib import admin
from .models import Franquia, Item_pedido, Produto, Revendedor, Pedido, Supervisor

admin.site.register(Revendedor)
admin.site.register(Produto)
admin.site.register(Pedido)
admin.site.register(Item_pedido)
admin.site.register(Supervisor)
admin.site.register(Franquia)