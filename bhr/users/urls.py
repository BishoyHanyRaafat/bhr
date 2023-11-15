from django.urls import path , include
from .views import home,favicon,permission_denied_view
from django.conf import settings
from django.conf.urls.static import static

handler403 = permission_denied_view
urlpatterns = [
    path('', home),
    path("home",home),
    path('', include('django.contrib.auth.urls')),
    #path('sign-up', sign_up, name='sign_up'),
    path("favicon.ico",favicon),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)