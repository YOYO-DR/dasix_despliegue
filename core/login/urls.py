from core.login.views import *
from django.urls import path

urlpatterns = [
    path('', LoginFormView.as_view(), name='login'),
    #path('logout/', LogoutView.as_view(), name='logout'),
    path('logout/', LogoutRedirectView.as_view(), name='logout'),
    path('recuperacion/', OlvidoContraEmailView.as_view(), name='recuperacion'),
    path('recuperacion-cambio/<uidb64>/<token>/', CambioContraView.as_view(), name='recuperacion-cambio'),
]