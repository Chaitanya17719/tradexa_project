from django.contrib import admin

from .models import Product, Box, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "sku",
        "length",
        "width",
        "height",
        "weight",
    )

    search_fields = (
        "name",
        "sku",
    )


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "length",
        "width",
        "height",
        "max_weight",
        "cost",
    )

    search_fields = (
        "name",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "order_number",
        "customer_name",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "order_number",
        "customer_name",
    )

    readonly_fields = (
        "created_at",
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "order",
        "product",
        "qty",
    )

    search_fields = (
        "order__order_number",
        "product__name",
    )