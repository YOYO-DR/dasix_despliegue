from django.urls import path
from core.inventario.views.categoria.views import *
from core.inventario.views.cliente.views import *
from core.inventario.views.compra.views import CompraCreateView, CompraDeleteView, CompraListView, CompraUpdateView
from core.inventario.views.proveedor.views import ProveedorCreateView, ProveedorDeleteView, ProveedorListView, ProveedorUpdateView
from core.inventario.views.venta.views import *
from core.inventario.views.dashboard.views import *
from core.inventario.views.producto.views import *

app_name = 'inventario'

urlpatterns = [
    #Categoria
    path('categoria/list/', CategoriaListView.as_view(), name='categoria_list'),
    path('categoria/add/', CategoriaCreateView.as_view(), name='categoria_create'),
    path('categoria/update/<int:pk>/', CategoriaUpdateView.as_view(), name='categoria_update'),
    path('categoria/delete/<int:pk>/', CategoriaDeleteView.as_view(), name='categoria_delete'),

    # producto
    path('producto/list/', ProductoListView.as_view(), name='producto_list'),
    path('producto/add/', ProductoCreateView.as_view(), name='producto_create'),
    path('producto/update/<int:pk>/', ProductoUpdateView.as_view(), name='producto_update'),
    path('producto/delete/<int:pk>/', ProductoDeleteView.as_view(), name='producto_delete'),

    # cliente
    path('cliente/list/', ClienteListView.as_view(), name='cliente_list'),
    path('cliente/add/', ClienteCreateView.as_view(), name='cliente_create'),
    path('cliente/update/<int:pk>/', ClienteUpdateView.as_view(), name='cliente_update'),
    path('cliente/delete/<int:pk>/', ClienteDeleteView.as_view(), name='cliente_delete'),

    # proveedor
    path('proveedor/list/', ProveedorListView.as_view(), name='proveedor_list'),
    path('proveedor/add/', ProveedorCreateView.as_view(), name='proveedor_create'),
    path('proveedor/update/<int:pk>/', ProveedorUpdateView.as_view(), name='proveedor_update'),
    path('proveedor/delete/<int:pk>/', ProveedorDeleteView.as_view(), name='proveedor_delete'),

    # compra
    path('compra/list/', CompraListView.as_view(), name='compra_list'),
    path('compra/add/', CompraCreateView.as_view(), name='compra_create'),
    path('compra/update/<int:pk>/', CompraUpdateView.as_view(), name='compra_update'),
    path('compra/delete/<int:pk>/', CompraDeleteView.as_view(), name='compra_delete'),

    #Home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    #Venta
    path('venta/list/', VentaListView.as_view(), name='venta_list'),
    path('venta/add/', VentaCreateView.as_view(), name='venta_create'),
    path('venta/delete/<int:pk>/', VentaDeleteView.as_view(), name='venta_delete'),
    path('venta/update/<int:pk>/', VentaUpdateView.as_view(), name='venta_update'),

    
]        