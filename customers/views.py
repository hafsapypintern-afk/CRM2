from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from .models import Customer
from .tasks import send_customer_email


# ============================================================
# CUSTOMER LIST
# ============================================================

class CustomerListView(ListView):
    # Model used by this view.
    model = Customer

    # Use the custom manager defined in models.py.
    # This allows us to use Customer.customers instead of
    # Django's default Customer.objects manager.
    queryset = Customer.customers.all()

    # Template used to display all customers.
    template_name = "customers/customer_list.html"

    # Variable name available inside the template.
    context_object_name = "customers"


# ============================================================
# CUSTOMER DETAIL
# ============================================================

class CustomerDetailView(DetailView):
    # Model used by this view.
    model = Customer

    # Use the custom manager.
    queryset = Customer.customers.all()

    # Template used to display one customer's details.
    template_name = "customers/customer_detail.html"

    # Variable name available inside the template.
    context_object_name = "customer"

    def get_context_data(self, **kwargs):
        # Get the normal context provided by DetailView.
        context = super().get_context_data(**kwargs)

        # self.object is the Customer being viewed.
        # orders is the related manager created by the
        # relationship between Customer and Order.
        # .all() gets all orders belonging to this customer.
        context["orders"] = self.object.orders.all()

        return context


# ============================================================
# CUSTOMER CREATE
# ============================================================

class CustomerCreateView(CreateView):
    # Model that will be created.
    model = Customer

    # Fields displayed in the creation form.
    fields = [
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "address",
        "city",
    ]

    # Template used for the creation form.
    template_name = "customers/customer_form.html"

    # Redirect here after successfully creating a customer.
    success_url = reverse_lazy("customer_list")

    def form_valid(self, form):
        # Let CreateView validate and save the customer first.
        # After this line, self.object contains the newly
        # created Customer object.
        response = super().form_valid(form)

        # Send the welcome email through Celery.
        # .delay() sends the task to Redis, and the Celery
        # worker processes it in the background.
        #
        # We pass the customer's first name and email address
        # to the task.
        send_customer_email.delay(
            self.object.first_name,
            self.object.email
        )

        # Return the normal CreateView response so Django
        # redirects the user to success_url.
        return response


# ============================================================
# CUSTOMER UPDATE
# ============================================================

class CustomerUpdateView(UpdateView):
    # Model that will be updated.
    model = Customer

    # Fields that can be edited.
    fields = [
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "address",
        "city",
    ]

    # Reuse the customer form template.
    template_name = "customers/customer_form.html"

    # Variable name available inside the template.
    context_object_name = "customer"

    def get_success_url(self):
        # After updating, go to this customer's detail page.
        return reverse_lazy(
            "customer_detail",
            kwargs={"pk": self.object.pk}
        )


# ============================================================
# CUSTOMER DELETE
# ============================================================

class CustomerDeleteView(DeleteView):
    # Model that will be deleted.
    model = Customer

    # Template used to confirm deletion.
    template_name = "customers/customer_confirm_delete.html"

    # Variable name available inside the template.
    context_object_name = "customer"

    # Redirect to the customer list after deletion.
    success_url = reverse_lazy("customer_list")
