from django.contrib import admin
from django.urls import path
# from .views import
from django.conf import settings
from django.conf.urls.static import static
from.views import discounts,new_voucher,vouchers,moneyback


urlpatterns = [
    path('', discounts),
    path('moneyback/',moneyback),
    path('vouchers/<int:voucher>',new_voucher),
    path('vouchers/',vouchers),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)