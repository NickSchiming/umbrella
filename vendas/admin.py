from django.contrib import admin
from .models import Produto, Revendedor

admin.site.register(Revendedor)
admin.site.register(Produto)
