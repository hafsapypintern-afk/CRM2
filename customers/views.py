from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer


def customer_list(request):
    customers = Customer.objects.all()

    return render(request,"customers/customer_list.html",{"customers": customers})

def customer_detail(request, id):

    customer = get_object_or_404(Customer,id=id)

    orders = customer.orders.all()

    return render(request,"customers/customer_detail.html",
        {
            "customer": customer,
            "orders": orders,
        }
    )


def customer_create(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        phone_number = request.POST["phone_number"]
        address = request.POST["address"]
        city = request.POST["city"]

        Customer.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            address=address,
            city=city
        )

        return redirect("customer_list")

    return render(
        request,
        "customers/customer_form.html"
    )


def customer_update(request, id):
    customer = get_object_or_404(Customer, id=id)

    if request.method == "POST":
        customer.first_name = request.POST["first_name"]
        customer.last_name = request.POST["last_name"]
        customer.email = request.POST["email"]
        customer.phone_number = request.POST["phone_number"]
        customer.address = request.POST["address"]
        customer.city = request.POST["city"]

        customer.save()

        return redirect("customer_detail", id=customer.id)

    return render(
        request,
        "customers/customer_form.html",
        {"customer": customer}
    )


def customer_delete(request, id):
    customer = get_object_or_404(Customer, id=id)

    if request.method == "POST":
        customer.delete()
        return redirect("customer_list")

    return render(
        request,
        "customers/customer_confirm_delete.html",
        {"customer": customer}
    )