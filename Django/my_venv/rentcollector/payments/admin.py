from django.contrib import admin
from .models import Tenant, RentPayment


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number')


@admin.register(RentPayment)
class RentPaymentAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'amount', 'paid', 'created_at')
    list_filter = ('paid',)
