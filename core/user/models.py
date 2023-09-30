import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import model_to_dict
from config.settings import MEDIA_URL, STATIC_URL

AZURE_STATIC="https://contenedordasix.blob.core.windows.net/django-dasix"+STATIC_URL

class User(AbstractUser):
    email = models.EmailField(unique=True,null=False,blank=False,verbose_name="Email")
    if "WEBSITE_HOSTNAME" in os.environ:
        image=models.ImageField(upload_to=f'{MEDIA_URL}users/%Y/%m/%d', null=True, blank=True)
    else:
        image=models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True)

    def get_image(self):
        if self.image:
            return self.image.url
        if "WEBSITE_HOSTNAME" in os.environ:
            return '{}{}'.format(AZURE_STATIC, 'img/empty.png')
        else:
            return '{}{}'.format(STATIC_URL, 'img/empty.png')
    
    def toJSON(self):
        item = model_to_dict(self, exclude=['password', 'user_permissions', 'last_login'])
        item['username']=self.username
        item["image"]=self.get_image()
        if self.last_login:
            item['last_login'] = self.last_login.strftime('%Y-%m-%d')
        item['Date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['groups']=[group.name for group in self.groups.all()]
        return item