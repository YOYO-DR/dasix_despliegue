from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth import authenticate
from core.inventario.mixins import ValidatePermissionRequiredMixin
from core.user.forms import UserForm
from core.user.models import User

class UserListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    permission_required='user.view_user'
    model=User
    template_name='user/list.html'
    url_redirect=reverse_lazy("inventario:dashboard")

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data={}
        try:
            action=request.POST['action']
            if action =='searchdata':
                data=[]
                for i in User.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] ='No ha ingresado a ninguna opcion'
        except Exception as e:
            data={}
            data['error']=str (e)
        return JsonResponse(data, safe=False)
    

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['title']='Listado de usuarios'
        context['create_url']=reverse_lazy('user:user_create')
        context['list_url']=reverse_lazy('user:user_list')
        context['entity']='Usuarios'
        return context

class UserCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('user:user_list')
    permission_required = 'user.add_user'
    url_redirect = success_url

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
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de un Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

class UserUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('user:user_list')
    permission_required = 'user.change_user'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de un Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class UserDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model=User
    template_name='user/delete.html'
    success_url=reverse_lazy('user:user_list')
    permission_required = 'user.delete_user'
    url_redirect = success_url

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
        context['title'] = 'Eliminacion de un Usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        return context

class UserCambioContrasena(LoginRequiredMixin,View):
  def post(self, request, *args, **kwargs):
      data={}
      #contraseñas
      password=request.POST.get("password",None)
      password1=request.POST.get("password1",None)
      password2=request.POST.get("password2",None)
      # verificar que envie la contraseña actual
      if not password:
        return JsonResponse({"error":"No se envio la contraseña actual"})
      
      # verifico que haya enviado las 2 contraseñas para cambiar
      if not (password1 and password2):
          return JsonResponse({"error":"Falta alguna de las confirmaciones de la contraseña nueva"})
      
      # verificamos que la contraseña actual sea correcta
      user=authenticate(request, username=request.user.username, password=password)
      if not user:
        return JsonResponse({"error":"Contraseña incorrecta"})
      
      # verificar que las 2 contraseñas sean iguales
      if not password1 == password2:
          return JsonResponse({"error":"Las contraseñas no coinciden"})
      
      # verificar que sean mayor a 8 caracteres
      if len(password1)<8:
          return JsonResponse({"error":"La contraseña tener 8 o más caracteres"})
      
      user.set_password(password1)
      user.save()
      return JsonResponse(data)