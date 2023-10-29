from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.

class IPAddress(models.Model):
    users = models.ManyToManyField(User)
    address = models.GenericIPAddressField(protocol='both')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address