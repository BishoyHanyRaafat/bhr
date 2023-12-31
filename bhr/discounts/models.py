from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import uuid
# Create your models here.
def add_year():
    return timezone.now() + timedelta(days=365)
def add_weak():
    return timezone.now() + timedelta(days=7)
class Voucher(models.Model):
    voucher_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()
    create_date = models.DateField(auto_now_add=True)
    expire_date = models.DateField(default=add_weak)
    is_used = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user}-{self.value}"

class Point(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()
    create_date = models.DateField(auto_now_add=True)
    expire_date = models.DateField(default=add_year)
    def __str__(self):
        return f"{self.user} - {self.value}  'From {self.create_date} to {self.expire_date}'"
