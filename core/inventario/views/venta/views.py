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

class VentaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Venta
    template_name = 'venta/list.html'
    permission_required = 'inventario.view_venta'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Venta.objects.all():
                    data.append(i.toJSON())
            elif action=='search_detalle_produ':
                data=[]
                for i in DetalleVenta.objects.filter(Venta_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data={}
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ventas'
        context['create_url'] = reverse_lazy('inventario:venta_create')
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

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
         return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search-productos':
                data=[]
                ids_exclude=json.loads(request.POST['ids'])
                print(ids_exclude)
                produ=Producto.objects.filter(Nombre__icontains=request.POST['term'], Stock__gt=0)
                for i in produ.exclude(id__in=ids_exclude)[0:10]:
                    item=i.toJSON()
                    #item['value']=i.Nombre
                    item['text']=i.Nombre
                    data.append(item)
            elif action=='add':
                # El transaction.atomic sirve para cuando hay un error no se guarde solo una parte, la funcion
                # devuelve la accion hasta el principio y no se guarda nada
                with transaction.atomic():
                    ventas=json.loads(request.POST['ventas'])

                    venta=Venta()
                    venta.Date_joined=ventas['Date_joined']
                    venta.Cli_id=ventas['Cli']
                    venta.Subtotal=float(ventas['Subtotal'])
                    venta.Iva=float(ventas['Iva'])
                    venta.Total=float(ventas['Total'])
                    venta.save()

                    for i in ventas['productos']:
                        det=DetalleVenta()
                        det.Venta_id=venta.id
                        det.Produ_id=i['id']
                        det.Cantidad=int(i['Cantidad'])
                        det.Precio=float(i['pvp'])
                        det.Subtotal=float(i['Subtotal'])
                        det.save()

                        det.Produ.Stock -= det.Cantidad
                        det.Produ.save()
            else:
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

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search-productos':
                data = []
                ids_exclude=json.loads(request.POST['ids'])
                print(ids_exclude)
                prods = Producto.objects.filter(Nombre__icontains=request.POST['term'],Stock__gt=0)
                for i in prods.exclude(id__in=ids_exclude)[0:10]:
                    item = i.toJSON()
                    item['value'] = i.Nombre
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    ventas = json.loads(request.POST['ventas'])
                    #venta = Venta.objects.get(pk=self.get_object().id)
                    venta = self.get_object()
                    venta.Date_joined = ventas['Date_joined']
                    venta.Cli_id = ventas['Cli']
                    venta.Subtotal = float(ventas['Subtotal'])
                    venta.Iva = float(ventas['Iva'])
                    venta.Total = float(ventas['Total'])
                    venta.save()
                    venta.detalleventa_set.all().delete()
                    for i in ventas['productos']:
                        det = DetalleVenta()
                        det.Venta_id = venta.id
                        det.Produ_id = i['id']
                        det.Cantidad = int(i['Cantidad'])
                        det.Precio = float(i['pvp'])
                        det.Subtotal = float(i['Subtotal'])
                        det.save()

                        det.Produ.Stock -= det.Cantidad
                        det.Produ.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
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
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
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