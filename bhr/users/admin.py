from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import IPAddress
from django.urls import reverse
from django.utils.safestring import mark_safe
from discounts.models import Point,Voucher
from django.db import models
admin.site.site_header = 'BHR'
admin.site.site_title = 'BHR Admin'


class PointInline(admin.TabularInline):
    model = Point
    extra = 0
class VoucherInline(admin.TabularInline):
    model = Voucher
    extra = 0
class IPAddressAdmin(admin.ModelAdmin):
    list_display = ('address', "get_related_field",'created_at')
    search_fields = ('address','users__username')

    def get_related_field(self, obj):
        users = obj.users.all()
        user_links = [
            '<a href="{}">{}</a>'.format(
                reverse('admin:auth_user_change', args=(user.id,)), user.username
            )
            for user in users
        ]
        return mark_safe(", ".join(user_links))
    get_related_field.short_description = 'Users'

    class CustomDuplicateUsersFilter(admin.SimpleListFilter):
        title = 'Duplicated Users'
        parameter_name = 'is_duplicate'

        def lookups(self,request, _):
            return (
                ('true', 'Yes'),
                ('false', 'No'),
            )

        def queryset(self, _, queryset):
            if self.value() == 'true':
                # Filter to display IPAddress instances with duplicated users
                duplicate_user_ids = self.get_duplicate_user_ids()
                return queryset.filter(users__in=duplicate_user_ids)
            elif self.value() == 'false':
                # Filter to display IPAddress instances without duplicated users
                duplicate_user_ids = self.get_duplicate_user_ids()
                return queryset.exclude(users__in=duplicate_user_ids)

        def get_duplicate_user_ids(self):
            # Retrieve user IDs associated with multiple IPAddress instances
            duplicate_user_ids = IPAddress.objects.values('users').annotate(
                user_count=models.Count('users')
            ).filter(user_count__gt=1).values_list('users', flat=True)
            return duplicate_user_ids
    list_filter = (CustomDuplicateUsersFilter,)

class IPAddressInline(admin.TabularInline):
    model = IPAddress.users.through 
    extra = 0
    verbose_name = "IP Addresses"
    
    def user_link(self, obj):
        users = obj.ipaddress.users.exclude(id=obj.user.id)
        user_links = [
            '<a href="{}">{}</a>'.format(
                reverse('admin:auth_user_change', args=(user.id,)), user.username
            )
            for user in users
        ]
        return mark_safe(", ".join(user_links))
    user_link.short_description = 'Other users'
    readonly_fields = ("user_link",)

class CustomUserAdmin(UserAdmin):
    
    inlines = [PointInline,VoucherInline,IPAddressInline]

admin.site.register(IPAddress,IPAddressAdmin)

admin.site.unregister(User)
admin.site.register(User,CustomUserAdmin)
