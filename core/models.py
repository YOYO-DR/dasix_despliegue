from django.db import models
from django.conf import settings

class BaseModel(models.Model):
    user_creation=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='%(app_label)s_%(class)s_creation', null=True)
    date_creation=models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_update=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='%(app_label)s_%(class)s_updated', null=True)
    date_update=models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract= True
        
