"""
WSGI config for app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

# configuracion del servidor sincrono
import os

from django.core.wsgi import get_wsgi_application

# cambia de config a production dependiendo si estamos en desarrollo o produccion
settings_module = 'config.production' if 'WEBSITE_HOSTNAME' in os.environ else 'config.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
