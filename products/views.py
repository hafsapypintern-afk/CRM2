from django.shortcuts import render, redirect, get_object_or_404

from .models import Product


def product_list(request):

    products = Product.objects.all()

    return render(
        request,
        "products/product_list.html",
        {"products": products}
    )


def product_detail(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    return render(
        request,
        "products/product_detail.html",
        {"product": product}
    )


def product_create(request):

    if request.method == "POST":

        product_name = request.POST["product_name"]
        product_description = request.POST["product_description"]
        product_price = request.POST["product_price"]
        stock = request.POST["stock"]

        Product.objects.create(
            product_name=product_name,
            product_description=product_description,
            product_price=product_price,
            stock=stock
        )

        return redirect("product_list")

    return render(
        request,
        "products/product_form.html"
    )


def product_update(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    if request.method == "POST":

        product.product_name = request.POST["product_name"]
        product.product_description = request.POST["product_description"]
        product.product_price = request.POST["product_price"]
        product.stock = request.POST["stock"]

        product.save()

        return redirect(
            "product_detail",
            id=product.id
        )

    return render(
        request,
        "products/product_form.html",
        {"product": product}
    )


def product_delete(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    if request.method == "POST":

        product.delete()

        return redirect("product_list")

    return render(
        request,
        "products/product_confirm_delete.html",
        {"product": product}
    )
