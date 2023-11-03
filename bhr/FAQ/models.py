from django.db import models

# Create your models here.
class FAQ(models.Model):
    question_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    def __str__(self) -> str:
        return self.title