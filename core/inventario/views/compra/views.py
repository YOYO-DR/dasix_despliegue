from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.inventario.mixins import ValidatePermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from core.inventario.forms import CompraForm
from core.inventario.models import Compra


class CompraListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Compra
    template_name = 'compra/list.html'
    permission_required = 'inventario.view_compra'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data={}
        try:
            action=request.POST['action']
            if action =='searchdata':
                data=[]
                for i in Compra.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] ='Ha ocurrido un error'
        except Exception as e:
            data={}
            data['error']=str (e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Compras'
        context['create_url'] = reverse_lazy('inventario:compra_create')
        context['list_url'] = reverse_lazy('inventario:compra_list')
        context['entity'] = 'Compras'
        return context


class CompraCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Compra
    form_class = CompraForm
    template_name = 'compra/create.html'
    success_url = reverse_lazy('inventario:compra_list')
    permission_required = 'inventario.add_compra'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data={}
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Compra'
        context['entity'] = 'Compras'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class CompraUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Compra
    form_class = CompraForm
    template_name = 'compra/create.html'
    success_url = reverse_lazy('inventario:compra_list')
    permission_required = 'inventario.change_compra'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                # pregunto si se cambio la cantidad
                cantidad_anterior=form.initial.get("Cantidad")
                cantidad_nueva=int(form.data.get("Cantidad"))
                if cantidad_anterior!=cantidad_nueva:
                    # pregunto si se mermo o aumento
                    # si aumento, hago la resta para aumentar ese valor al producto
                    if cantidad_anterior<cantidad_nueva:
                        form.instance.Producto.Stock+=cantidad_nueva-cantidad_anterior
                    # si disminuyo, hago la resta al revez para restarle esa diferencia al producto
                    else:
                        form.instance.Producto.Stock-=cantidad_anterior-cantidad_nueva
                        if form.instance.Producto.Stock<0:
                            form.instance.Producto.Stock=0
                    form.instance.Producto.save()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data={}
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Compra'
        context['entity'] = 'Compras'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class CompraDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Compra
    template_name = 'compra/delete.html'
    success_url = reverse_lazy('inventario:compra_list')
    permission_required = 'inventario.delete_compra'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
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
        context['title'] = 'Eliminación de una Compra'
        context['entity'] = 'Compras'
        context['list_url'] = self.success_url
        return context