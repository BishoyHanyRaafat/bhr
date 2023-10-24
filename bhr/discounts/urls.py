from django.contrib import admin
from django.urls import path
# from .views import
from django.conf import settings
from django.conf.urls.static import static
from.views import discounts,new_voucher,vouchers,moneyback,voucher_admin,user_QR


urlpatterns = [
    path('', discounts),
    path('moneyback/',moneyback),
    path('vouchers/<int:voucher>',new_voucher),
    path('vouchers/',vouchers),
    path('vouchers/admin/<str:voucher_id>',voucher_admin),
    path('users/<int:user_id>',user_QR),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)