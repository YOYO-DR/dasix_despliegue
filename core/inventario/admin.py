from django.contrib import admin
from core.inventario.models import *

# Registrar los modelos en el admin para que aparezcan en el administrador de django
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Cliente)
admin.site.register(Proveedor)
admin.site.register(Compra)
admin.site.register(Venta)
admin.site.register(DetalleVenta)