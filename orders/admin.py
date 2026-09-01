from django.contrib import admin

from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "customer",
        "order_date",
        "status",
    )

    search_fields = (
        "customer__first_name",
        "customer__last_name",
        "customer__email",
    )

    list_filter = (
        "status",
        "order_date",
    )

    ordering = (
        "-order_date",
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order",
        "product",
        "quantity",
        "unit_price",
    )

    search_fields = (
        "product__product_name",
    )

    list_filter = (
        "product",
    )