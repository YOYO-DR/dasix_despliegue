from core.inventario.models import *
from django.views.generic import *
from django.utils.decorators import *
from django.http import *
from django.views.decorators.csrf import *
from core.inventario.forms import *
from django.urls import *
from django.contrib.auth.decorators import * 
from core.inventario.mixins import ValidatePermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
# El LoginRequiredMixin es para validar que este Logueado
# El ValidatePermissionRequiredMixin validar los permisos para entrar a la vista

class CategoriaListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    # este atributo es para ponerle el nombre al permiso de esta vista, para que cuando se cree un grupo de permisos
    permission_required='inventario.view_categoria'
    model=Categoria
    template_name='categoria/list.html'

    # esta funcion es la que manipula las peticiones por el metodo "POST"
    def post(self, request, *args, **kwargs):
        data={}
        try:
            # obtengo la accion de la peticion
            action=request.POST['action']
            if action =='searchdata':
                # aqui retorno todas las categorias y les pongo su metodo toJSON para convertirlo en diccionario y se pueda serializar (convertir a JSON)
                data=[]
                for i in Categoria.objects.all():
                    data.append(i.toJSON())
            else:
                # si no se envia el action, retorno el error
                data['error'] ='No ha ingresado a ninguna opcion'
        except Exception as e:
            # si hay un error en el codigo, lo envio
            data={}
            data['error']=str (e)
        return JsonResponse(data, safe=False)
    
    # esta funcion es para enviar valores al template
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['title']='Listado de categorias'
        # el reverse_lazy es para obtener alguna url por su nombre ("app:name_url"), y retorna la url completa (https://...)
        context['create_url']=reverse_lazy('inventario:categoria_create')
        context['list_url']=reverse_lazy('inventario:categoria_list')
        context['entity']='Categorias'
        return context
    
class CategoriaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model=Categoria
    form_class=CategoriaForm
    template_name='categoria/create.html'
    success_url=reverse_lazy('inventario:categoria_list')
    permission_required = 'inventario.add_categoria'
    url_redirect = success_url

    #@method_decorator(csrf_exempt)
    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data={}
        try:
            action=request.POST['action']
            if action == 'add':
                form=self.get_form()
                data=form.save()
            else:
                data['error']='No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error']=str (e)
        return JsonResponse(data)

    #     print(request.POST)
    #     form = CategoriaForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponseRedirect(self.success_url)
    #     self.object = None
    #     context = self.get_context_data(**kwargs)
    #     context['form'] = form
    #     return render(request, self.template_name, context

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['title']='Creacion de categorias'
        context['entity']='Categorias'
        context['list_url']=self.success_url
        context['action']='add'
        return context 

class CategoriaUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model=Categoria
    form_class=CategoriaForm
    template_name='categoria/create.html'
    success_url=reverse_lazy('inventario:categoria_list')
    permission_required = 'inventario.change_category'
    url_redirect = success_url

    #@method_decorator(csrf_exempt)
    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object=self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data={}
        try:
            action=request.POST['action']
            if action == 'edit':
                form=self.get_form()
                data=form.save()
            else:
                data['error']='No ha ingresado a ninguna opcion'
        except Exception as e:
            data={}
            data['error']=str (e)

        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['title']='Edicion de categorias'
        context['entity']='Categorias'
        context['list_url']=self.success_url
        context['action']='edit'
        return context 
    
class CategoriaDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model=Categoria
    template_name='categoria/delete.html'
    success_url=reverse_lazy('inventario:categoria_list')
    permission_required = 'inventario.delete_category'
    url_redirect = success_url

    #@method_decorator(csrf_exempt)
    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object=self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data={}
        try:
            self.object.delete()
        except Exception as e:
            data['error']=str(e)
        return JsonResponse(data)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminacion de una Categoria'
        context['entity'] = 'Categorias'
        context['list_url'] = self.success_url
        return context