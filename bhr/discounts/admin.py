from django.contrib import admin
from .models import Point,Voucher
# Register your models here.

@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ('user', 'value', 'create_date', 'expire_date')
    list_filter = ('expire_date',)
    search_fields = ('user__username',)

@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ('user', 'value', 'create_date', 'expire_date')
    list_filter = ('is_used','expire_date', 'value')
    search_fields = ('user__username','voucher_id')
