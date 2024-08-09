from django.contrib import admin
from .models import Cart, Tax


class Cart_Admin(admin.ModelAdmin):
    list_display = ('user', 'fooditem', 'quantity', 'updated_at')


class TaxAdmin(admin.ModelAdmin):
    list_display = ('tax_type', 'tax_percentage', 'is_active')


admin.site.register(Cart, Cart_Admin)
admin.site.register(Tax, TaxAdmin)
