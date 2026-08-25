
from django.shortcuts import render, redirect, get_object_or_404

from .models import Order, OrderItem
from customers.models import Customer
from products.models import Product


def order_list(request):
    orders = Order.objects.all()

    return render(
        request,
        "orders/order_list.html",
        {"orders": orders}
    )


def order_detail(request, id):

    order = get_object_or_404(
        Order,
        id=id
    )

    items = order.items.all()

    return render(
        request,
        "orders/order_detail.html",
        {
            "order": order,
            "items": items,
        }
    )


def order_create(request):

    if request.method == "POST":

        customer_id = request.POST["customer"]
        status = request.POST["status"]

        customer = get_object_or_404(
            Customer,
            id=customer_id
        )

        # Create the Order first
        order = Order.objects.create(
            customer=customer,
            status=status
        )

        # Get selected products
        product_ids = request.POST.getlist("products")

        # Create OrderItems
        for product_id in product_ids:

            product = get_object_or_404(
                Product,
                id=product_id
            )

            quantity = request.POST.get(
                f"quantity_{product_id}"
            )

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                unit_price=product.product_price
            )

        return redirect(
            "order_detail",
            id=order.id
        )

    customers = Customer.objects.all()
    products = Product.objects.all()

    return render(
        request,
        "orders/order_form.html",
        {
            "customers": customers,
            "products": products,
        }
    )


def order_update(request, id):

    order = get_object_or_404(
        Order,
        id=id
    )

    if request.method == "POST":

        customer_id = request.POST["customer"]
        status = request.POST["status"]

        customer = get_object_or_404(
            Customer,
            id=customer_id
        )

        order.customer = customer
        order.status = status

        order.save()

        return redirect(
            "order_detail",
            id=order.id
        )

    customers = Customer.objects.all()

    return render(
        request,
        "orders/order_form.html",
        {
            "order": order,
            "customers": customers
        }
    )


def order_delete(request, id):

    order = get_object_or_404(
        Order,
        id=id
    )

    if request.method == "POST":

        order.delete()

        return redirect("order_list")

    return render(
        request,
        "orders/order_confirm_delete.html",
        {"order": order}
    )
