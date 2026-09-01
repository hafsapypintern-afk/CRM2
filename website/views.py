from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, F, Sum, Count
from django.views import View
from django.views.generic import TemplateView

from .forms import RegisterForm

from customers.models import Customer
from products.models import Product
from orders.models import Order


# =========================================================
# HOME
# =========================================================

class HomeView(View):

    def get(self, request):

        # If the user is already logged in,
        # send them directly to the dashboard.
        if request.user.is_authenticated:
            return redirect("dashboard")

        # Show the home page.
        return render(
            request,
            "home.html"
        )


# =========================================================
# LOGIN
# =========================================================

class LoginView(View):

    def get(self, request):

        # If the user is already logged in,
        # there is no need to show the login page.
        if request.user.is_authenticated:
            return redirect("dashboard")

        # Show login page.
        return render(request,"login.html")

    def post(self, request):

        # Get username entered by the user.
        username = request.POST["username"]

        # Get password entered by the user.
        password = request.POST["password"]

        # Check whether the username and password
        # belong to a valid Django user.
        user = authenticate(request,username=username,password=password)

        # If authentication was successful.
        if user is not None:

            # Create a login session for the user.
            login(request, user)

            # Show success message.
            messages.success(request,"You are logged in!")

            # Send user to dashboard.
            return redirect("dashboard")

        # Authentication failed.
        messages.error(request,"Invalid username or password.")

        # Go back to login page.
        return redirect("login")


# =========================================================
# LOGOUT
# =========================================================

class LogoutView(View):

    def get(self, request):

        # Remove the user's login session.
        logout(request)

        # Show logout message.
        messages.success(request,"You have been logged out!")

        # Send user back to home page.
        return redirect("home")


# =========================================================
# REGISTER
# =========================================================

class RegisterView(View):

    def get(self, request):

        # Logged-in users should not register again.
        if request.user.is_authenticated:
            return redirect("dashboard")

        # Create an empty registration form.
        form = RegisterForm()

        # Show registration page.
        return render(request,"register.html",
            {
                "form": form
            }
        )

    def post(self, request):

        # Logged-in users should not register again.
        if request.user.is_authenticated:
            return redirect("dashboard")

        # Create form using submitted data.
        form = RegisterForm(request.POST)

        # Check whether submitted data is valid.
        if form.is_valid():

            # Save the new user.
            user = form.save()

            # Log the user in immediately.
            login(request, user)

            # Show success message.
            messages.success(request,"You have successfully registered!")

            # Send user to dashboard.
            return redirect("dashboard")

        # If form is invalid,
        # show the form again with errors.
        return render(
            request,
            "register.html",
            {
                "form": form
            }
        )


# =========================================================
# DASHBOARD GCBV
# =========================================================

# TemplateView is a Django Generic Class-Based View (GCBV).
# DashboardView inherits from TemplateView.
# Therefore DashboardView is a GCBV.
# This is not a CRUD view.
# It is a GCBV used to display a template with custom data.
class DashboardView(LoginRequiredMixin, TemplateView):

    # Tell TemplateView which HTML file to render.
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):

        # Get the context dictionary created by TemplateView.
        # We will add our own dashboard data to it.
        context = super().get_context_data(**kwargs)


        # =================================================
        # BASIC COUNTS
        # =================================================

        # Count all customers.
        customer_count = Customer.customers.count()

        # Count all products.
        product_count = Product.objects.count()

        # Count all orders.
        order_count = Order.objects.count()


        # =================================================
        # RECENT CUSTOMERS
        # =================================================

        # Get the 5 most recently created customers. -created_at means newest first.
        # [:5] means only get 5 customers.
        recent_customers = (Customer.customers.order_by("-created_at")[:5])

        # =================================================
        # FILTERED CUSTOMERS
        # =================================================

        # Get customers from Lahore OR Islamabad.
        # Q() allows us to create complex queries.
        # __iexact means case-insensitive exact matching.
        filtered_customers = (Customer.customers
            .filter(Q(city__iexact="Lahore") |Q(city__iexact="Islamabad"))
        )


        # =================================================
        # RECENT ORDERS
        # =================================================

        # Get the 5 most recent orders.
        # select_related("customer") efficiently loads
        # the customer connected through the ForeignKey.
        recent_orders = (Order.objects.select_related("customer").order_by("-order_date")[:5])


        # =================================================
        # RECENT ORDERS WITH ITEMS AND PRODUCTS
        # =================================================

        # Get the 5 most recent orders.
        # select_related("customer")
        # gets the related customer efficiently.
        # prefetch_related("items__product")
        # gets the order items and their products efficiently.
        recent_orders_with_items = (Order.objects.select_related("customer").prefetch_related("items__product").order_by("-order_date")[:5])


        # =================================================
        # LOW STOCK PRODUCTS
        # =================================================

        # Find products where stock is less than 5.
        # stock__lt=5 means:
        # stock < 5
        # order_by("stock") puts the lowest stock first.
        low_stock_products = (Product.objects.filter(stock__lt=5).order_by("stock"))


        # =================================================
        # HIGHEST AMOUNT ORDERS
        # =================================================

        # Calculate the total amount of every order.
        # quantity × unit_price
        # F() allows us to refer to database fields.
        # Sum() adds the values of the order items.
        highest_amount_orders = (Order.objects.annotate(total_amount=Sum(
                    F("items__quantity") *
                    F("items__unit_price")
                )
            )
            .order_by("-total_amount")[:5]
        )


        # =================================================
        # MOST FREQUENT CUSTOMERS
        # =================================================

        # Count how many orders each customer has.
        # Count("orders") follows the relationship:
        # Customer → Orders
        # The calculated value is called order_count.
        frequent_customers = (
            Customer.customers
            .annotate(order_count=Count("orders"))
            .order_by("-order_count")[:5]
        )


        # =================================================
        # ADD DATA TO CONTEXT
        # =================================================

        # Add the data to the context dictionary.
        # These names will be available inside
        # dashboard.html.

        context["customer_count"] = customer_count

        context["product_count"] = product_count

        context["order_count"] = order_count

        context["recent_customers"] = recent_customers

        context["filtered_customers"] = filtered_customers

        context["recent_orders"] = recent_orders

        context["recent_orders_with_items"] = recent_orders_with_items

        context["low_stock_products"] = low_stock_products

        context["highest_amount_orders"] = highest_amount_orders

        context["frequent_customers"] = frequent_customers


        # Return the context to TemplateView.
        # TemplateView then renders dashboard.html
        # using this context.
        return context