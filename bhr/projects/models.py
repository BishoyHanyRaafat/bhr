from django.db import models

# Create your models here.
def project_image_path(instance, filename):
    return f'project_images/{instance.project.project_id}/{filename}'
class Certificate(models.Model):
    certificate_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='certificates/')
    def __str__(self):
        return self.title

class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    demo = models.BooleanField()
    chat = models.BooleanField()
    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=project_image_path)
    show = models.BooleanField(default=True)
    def __str__(self):
        return self.project.title
