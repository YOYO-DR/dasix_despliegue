from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import RedirectView,TemplateView
from core.user.models import User
from config import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
import os
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_bytes
from config.settings import EMAIL_HOST_USER
from core.login.funciones import validar_contra, validar_patron_correo
# se puede hacer cualquiera de las dos formas(loginformview o loginformview2)

class LoginFormView(LoginView):
    template_name='login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['title']='Iniciar sesion'
        return context

class LogoutRedirectView(RedirectView):
    pattern_name = 'login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)

class OlvidoContraEmailView(TemplateView):
  template_name="olvidoContra.html"

  def post(self, request, *args, **kwargs):
    datos={}
    #pregunto si se esta enviando el correo
    if request.POST.get('email'):
      #si existe, lo almaceno
      email = request.POST.get('email')
      #valido si es correcto
      if not validar_patron_correo(email):
        datos['error'] = "Debe ingresar un correo valido"
      else:
        # pregunto si existe un usuario con ese correo
        if not User.objects.filter(email=email).exists():
          datos['error'] = "No existe un usuario con ese correo"
        else:
          #obtengo el usuario con ese correo
          usuario=User.objects.get(email=email)
          #enviar correo
          dominio = get_current_site(request)
          if 'WEBSITE_HOSTNAME' in os.environ:
              dominio = 'https://'+str(dominio)
          else:
              dominio = 'http://'+str(dominio)
          asunto = 'Cambiar contraseña'
          cuerpoMensaje = render_to_string('email/olvidoContraEmail.html',{
              'usuario':usuario,
              'dominio':dominio,
              'uid':urlsafe_base64_encode(force_bytes(usuario.pk)),
              'token':default_token_generator.make_token(usuario)
          })
          toEmail = email
          envioEmail = EmailMultiAlternatives(asunto, '', to=[toEmail],from_email=f"Dasix <{EMAIL_HOST_USER}>")
          #luego con esa funcion le paso el html y le digo que va a ser un html
          envioEmail.attach_alternative(cuerpoMensaje, "text/html")
          envioEmail.send()
          datos['email']=usuario.email
    else:
      datos['error']="Debe ingresar un correo"

    return JsonResponse(datos)
  
class CambioContraView(TemplateView):
  template_name = "olvidoContraRecu.html"

  def dispatch(self, request, *args, **kwargs):
      if request.method == 'GET':
        uidb64=kwargs.get('uidb64')
        token=kwargs.get('token')
        try:
          #decodifico el uidb64 y obtengo el usuario segun el uid
          uid = urlsafe_base64_decode(uidb64).decode()
          usuario = User.objects.get(pk=uid)
        except (TypeError, ValueError,OverflowError, User.DoesNotExist):
          # si sale algun error, dejo el usuario como None
          usuario = None
        #si existe un usuario y el token es correcto, lo dejo entrar a la pagina
        #el token se va a invalidar cuando se le cambie la contraseña al usuario relacionado
        if usuario is not None and default_token_generator.check_token(usuario,token):
          pass
        # si ya expiro el token
        else:
          return redirect('login')
      return super().dispatch(request, *args, **kwargs)
  
  def post(self, request, *args, **kwargs):
    uid = urlsafe_base64_decode(kwargs.get('uidb64')).decode()
    usuario=User.objects.get(pk=uid)
    datos={}

    if not (request.POST.get('password1') and request.POST.get('password2')):
      #si estan vacias las contraseñas
      datos['error']="Las contraseñas no pueden estar vacias"
    else:
      #obtengo las contraseña ingresadas
      contra=request.POST.get('password1')
      contraConfirm=request.POST.get('password2')
      #verifico que sean iguales
      if contra != contraConfirm:
        datos['error']="Las contraseñas no coinciden"
      else:
        #valido la contraseña con el usuario para que no tenga cosas parecidas a sus datos
        validacionContra=validar_contra(contra,usuario)
        if not validacionContra[0]:
          #si hay errores en la verificacion
          if len(validacionContra[1])>1:
            mensaje=', '.join(validacionContra[1])
          else:
            mensaje=validacionContra[1][0]
          datos['error']=mensaje
        else:
          #cambio la contraseña
          usuario.set_password(contra)
          usuario.save()
    return JsonResponse(datos)
