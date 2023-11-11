from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class IPAddress(models.Model):
    users = models.ManyToManyField(User)
    address = models.GenericIPAddressField(protocol='both')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        app_label = 'auth'
        verbose_name = 'IP Address'
        verbose_name_plural = 'IP Addresses' 

    def __str__(self):
        return self.address