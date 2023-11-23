from django.contrib import admin
from .models import Project, ProjectImage, Certificate
# Register your models here.
class ImageInline(admin.TabularInline):  # or admin.StackedInline
    model = ProjectImage
    extra = 2  # the number of empty forms to display

class ProjectAdmin(admin.ModelAdmin):
    inlines = [ImageInline]

admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectImage)
admin.site.register(Certificate)
