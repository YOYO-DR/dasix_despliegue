from django.urls import path
from core.user.views import *


app_name = 'user'

urlpatterns = [
    #Usuario
    path('list/', UserListView.as_view(), name='user_list'),
    path('add/', UserCreateView.as_view(), name='user_create'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('cambio_contra/', UserCambioContrasena.as_view(), name='cambio_contra'),
    ]