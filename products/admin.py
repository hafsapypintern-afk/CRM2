from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "product_name",
        "product_price",
        "stock",
    )

    search_fields = (
        "product_name",
        "product_description",
    )

    list_filter = (
        "stock",
    )

    ordering = (
        "product_name",
    )