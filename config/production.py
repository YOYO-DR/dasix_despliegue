# para el despliegue en Azure

import os
from .settings import * #importamos todo
from .settings import BASE_DIR # importamos la ruta de inicio

# para poner la direccion permitida por el proyecto
ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []

CSRF_TRUSTED_ORIGINS = ['https://' + os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []

# lo ponemos en false porque ya no estamos en desarrollo, y en false no va a mostrar informacion importante
DEBUG = False

# esta config la pasa azure, agrega el whitenoise para los archivos estaticos
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Add whitenoise middleware after the security middleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Como se va a utilizar Azure Storage comentamos esto, porque esto es para que los archivos estaticos se utilicen desde el servidor mismo donde se despliega el proyecto
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# se obtiene la configuracion de la base de datos que le pasamos atravez de la configuracion de azure
conn_str = os.environ['AZURE_MYSQL_CONNECTIONSTRING']
conn_str_params = {pair.split('=')[0]: pair.split('=')[1] for pair in conn_str.split(' ')}

# asi esta la cadena que se pasa, y con el for anterior se estrae los datos y se guarda como diccionario
# AZURE_MYSQL_CONNECTIONSTRING=dbname=nombreBD host=elHost port=3306 sslmode=require user=usuario password=pass

# reescribimos la configuracion de la base de datos con los valores que le pasamos por Azure
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': conn_str_params['dbname'],
        'HOST': conn_str_params['host'],
        'USER': conn_str_params['user'],
        'PASSWORD': conn_str_params['password'],
    }
}

# configuracion del almacenamiento con Azure (Azure Storage)
azure_storage_blob = os.environ['AZURE_STORAGE_BLOB']
azure_storage_blob_parametros = {parte.split(' = ')[0]:parte.split(' = ')[1] for parte in azure_storage_blob.split('  ')}
# obtengo el diccionario de configuracion, igual como con la configuracion de la base de datos

# completo los valores de la cuenta de almacenamiento de azure
AZURE_CONTAINER = azure_storage_blob_parametros['container_name']
AZURE_ACCOUNT_NAME = azure_storage_blob_parametros['account_name']
AZURE_ACCOUNT_KEY = azure_storage_blob_parametros['account_key']

# le digo a Django que el almacenamiento se trabajara con azure, y le digo donde esta esas clases de configuracion, la cual estan el paquete (carpeta custom_storage), en el modulo (archivo custom_azure.py)
STORAGES = {
    "default": {"BACKEND": "storages.backends.azure_storage.AzureStorage"},
    "staticfiles": {"BACKEND": "custom_storage.custom_azure.PublicAzureStaticStorage"},
    "media": {"BACKEND": "custom_storage.custom_azure.PublicAzureMediaStorage"},
}

# este es el ejemplo de como llega la cadena que se configura en azure
#AZURE_STORAGE_BLOB = account_name = nombre_cuenta  container_name = nombre_contenedor  account_key = clave_cuenta