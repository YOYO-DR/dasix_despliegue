from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.inventario.mixins import ValidatePermissionRequiredMixin
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from core.inventario.models import Venta, Producto, DetalleVenta
from core.inventario.forms import VentaForm
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

# LoginRequiredMixin es para que valide que el usuario haya iniciado sesion
# ValidatePermissionRequiredMixin para validar los permisos, si el usuario no tiene permiso, lo redireciona al dashboard
class VentaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Venta
    template_name = 'venta/list.html'
    # creo el nombre de permiso para esta vista
    permission_required = 'inventario.view_venta'

    # funcion que trabaja las peticiones post de frontend
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            # Obtengo la accion a realizar
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                # si la accion es buscar todas las venta, retorno todas las ventas
                for i in Venta.objects.all():
                    data.append(i.toJSON())
            elif action=='search_detalle_produ':
                # aqui retorno todos los detalle de venta relacionados con el id de la venta que obtengo de la peticion post
                data=[]
                for i in DetalleVenta.objects.filter(Venta_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                # si no envia la accion, le retorno el error
                data={}
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            # si hay un error diferente, lo obtengo y lo retorno
            data={}
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # aqui pongo las variables para el template
        context['title'] = 'Listado de Ventas'
        # reveese_lazy toma el nombre de la url y retorna la url
        context['create_url'] = reverse_lazy('inventario:venta_create')
        # list_url sera la url de la lista del modelo
        context['list_url'] = reverse_lazy('inventario:venta_list')
        context['entity'] = 'Ventas'
        return context

class VentaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model= Venta
    form_class= VentaForm
    template_name='venta/create.html'
    success_url=reverse_lazy('inventario:venta_list')
    permission_required='inventario.add_venta'
    url_redirect=success_url

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search-productos':
                data=[]
                # si el usuario ya agrego ciertos productos a la lista para la venta, recibo esos ids y los excluyo de la busqueda que se realice
                ids_exclude=json.loads(request.POST['ids'])
                # busco los juegos por su nombre y que el stock sea mayor a 0
                produ=Producto.objects.filter(Nombre__icontains=request.POST['term'], Stock__gt=0)
                # excluyo los ids y solo tomo los 10 resultados
                for i in produ.exclude(id__in=ids_exclude)[0:10]:
                    item=i.toJSON()
                    # agrego una clave de "text" la cual select2 buscara para mostrar el resultado
                    item['text']=i.Nombre
                    data.append(item)
            elif action=='add':
                # El transaction.atomic sirve para cuando hay un error no se guarde solo una parte, la funcion
                # devuelve la accion hasta el principio y no se guarda nada
                with transaction.atomic():
                    # obtengo el diccionario de la venta a guardar
                    ventas=json.loads(request.POST['ventas'])

                    venta=Venta()# creo un objeto venta y le agrego todos los valores
                    venta.Date_joined=ventas['Date_joined']
                    venta.Cli_id=ventas['Cli']# le pongo Cli_id, porque ahi me estan mandando el id del cliente
                    venta.Subtotal=float(ventas['Subtotal'])
                    venta.Iva=float(ventas['Iva'])
                    venta.Total=float(ventas['Total'])
                    venta.save() # lo guardo para luego agregarle  sus detalle de venta

                    for i in ventas['productos']:
                        det=DetalleVenta()
                        det.Venta_id=venta.id
                        det.Produ_id=i['id']
                        det.Cantidad=int(i['Cantidad'])
                        det.Precio=float(i['pvp'])
                        det.Subtotal=float(i['Subtotal'])
                        det.save()# lo guardo para poder despues modificar el producto relacionado, ya que le pase el id en vez de un objeto Producto

                        det.Produ.Stock -= det.Cantidad # le disminuyo el stock al producto
                        if det.Produ.Stock<0:
                            det.Produ.Stock=0
                        det.Produ.save() # guardo los cambios en el producto
            else:
                data={}
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data={}
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

class VentaUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Venta
    form_class = VentaForm
    template_name = 'venta/create.html'
    success_url = reverse_lazy('inventario:venta_list')
    permission_required = 'inventario.change_venta'
    url_redirect = success_url

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search-productos':
                data = []
                ids_exclude=json.loads(request.POST['ids'])
                prods = Producto.objects.filter(Nombre__icontains=request.POST['term'],Stock__gt=0)
                for i in prods.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['value'] = i.Nombre
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    # obtengo la venta
                    ventas = json.loads(request.POST['ventas'])
                    # obtengo la venta a modificar y le agrego los nuevos valores
                    venta = self.get_object()
                    venta.Date_joined = ventas['Date_joined']
                    venta.Cli_id = ventas['Cli']
                    venta.Subtotal = float(ventas['Subtotal'])
                    venta.Iva = float(ventas['Iva'])
                    venta.Total = float(ventas['Total'])
                    venta.save() # lo guardo
                    # elimino todos los detalles de venta que tenga relacionados para agregarle los nuevos o modificados
                    venta.detalleventa_set.all().delete()
                    for i in ventas['productos']: # recorro los productos que se va a agregar
                        det = DetalleVenta()# creo un objeto de detalle de venta y agrego los valores
                        det.Venta_id = venta.id
                        det.Produ_id = i['id']
                        det.Cantidad = int(i['Cantidad'])
                        det.Precio = float(i['pvp'])
                        det.Subtotal = float(i['Subtotal'])
                        det.save()

                        det.Produ.Stock -= det.Cantidad
                        if det.Produ.Stock<0:
                            det.Produ.Stock=0
                        det.Produ.save()
            else:
                data={}
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data={}
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_detalles_producto(self):
        data = []
        try:
            for i in DetalleVenta.objects.filter(Venta_id=self.get_object().id):
                item = i.Produ.toJSON()
                item['Cantidad'] = i.Cantidad
                # pasarlos a flotantes porque los Decimal no se puede serializar
                item['pvp']=float(item['pvp'])
                item['Subtotal']=float(i.Subtotal)
                data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_detalles_producto())

        context['iva_por']=round(self.get_object().Iva / self.get_object().Subtotal,2)
        print(context['iva_por'])
        return context

class VentaDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Venta
    template_name = 'venta/delete.html'
    success_url = reverse_lazy('inventario:venta_list')
    permission_required = 'inventario.delete_venta'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object() # guardo el objeto actual en object y con la funcion get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            # elimino la venta, ella internamente elimina todos los detalle de venta que tenga relacionado
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        return context