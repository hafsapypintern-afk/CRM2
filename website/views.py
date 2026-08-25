from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import RegisterForm

from customers.models import Customer
from products.models import Product
from orders.models import Order


def home(request):

    # Already logged in → go to dashboard
    if request.user.is_authenticated:
        return redirect("dashboard")

    return render(request, "home.html")


def login_user(request):

    # Already logged in → don't show login page
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                "You are logged in!"
            )

            return redirect("dashboard")

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

            return redirect("login")

    return render(request, "login.html")


def logout_user(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out!"
    )

    return redirect("home")


def register_user(request):

    # Already logged in → don't show register page
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(
                request,
                "You have successfully registered!"
            )

            return redirect("dashboard")

    else:

        form = RegisterForm()

    return render(
        request,
        "register.html",
        {"form": form}
    )


def dashboard(request):

    # Not logged in → go to login
    if not request.user.is_authenticated:
        return redirect("login")

    customer_count = Customer.objects.count()
    product_count = Product.objects.count()
    order_count = Order.objects.count()

    recent_customers = Customer.objects.order_by(
        "-created_at"
    )[:5]

    return render(
        request,
        "dashboard.html",
        {
            "customer_count": customer_count,
            "product_count": product_count,
            "order_count": order_count,
            "recent_customers": recent_customers,
        }
    )
