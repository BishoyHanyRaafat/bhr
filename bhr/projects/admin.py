from django.contrib import admin
from .models import Project, ProjectImage, Certificate
# Register your models here.

admin.site.register(Project)
admin.site.register(ProjectImage)
admin.site.register(Certificate)
