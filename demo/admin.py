from django.contrib import admin
from demo import models


@admin.register(models.Supplier)
class CategoryAdmin(admin.ModelAdmin):
    list_filter = ['city', 'country']
    list_display = [
        'supplier_name',
        'contact_name',
        'phone',
        'address',
        'postal_code',
        'city',
        'country',
    ]


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_filter = ['city', 'country']
    list_display = [
        'customer_name',
        'contact_name',
        'address',
        'postal_code',
        'city',
        'country',
    ]


@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        'first_name',
        'last_name',
        'birth_date',
        'photo',
    ]


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'description']


@admin.register(models.Shipper)
class ShipperAdmin(admin.ModelAdmin):
    list_display = ['shipper_name', 'phone']


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ['category']
    list_display = ['product_name', 'category', 'unit', 'price']


class OrderDetailInline(admin.TabularInline):
    model = models.OrderDetail


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ['employee', 'shipper']
    list_display = ['id', 'customer', 'employee', 'shipper']
    inlines = [OrderDetailInline]
