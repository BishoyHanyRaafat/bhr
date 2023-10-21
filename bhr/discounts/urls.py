from django.contrib import admin
from django.urls import path
# from .views import
from django.conf import settings
from django.conf.urls.static import static
from.views import discounts


urlpatterns = [
    path('', discounts),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)