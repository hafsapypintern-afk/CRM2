from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, DeleteView, View

import logging

from .models import Order
from .forms import OrderItemFormSet

from customers.models import Customer


logger = logging.getLogger("crm")


# =========================================================
# ORDER LIST
# =========================================================

class OrderListView(ListView):

    # Model whose objects we want to display
    model = Order

    # Template used to display orders
    template_name = "orders/order_list.html"

    # Variable available inside the template
    context_object_name = "orders"


# =========================================================
# ORDER DETAIL
# =========================================================

class OrderDetailView(DetailView):

    # Model we want to display
    model = Order

    # Template used for order details
    template_name = "orders/order_detail.html"

    # Variable available inside the template
    context_object_name = "order"

    # URL uses <int:id>
    pk_url_kwarg = "id"

    def get_context_data(self, **kwargs):

        # Get normal DetailView context
        context = super().get_context_data(**kwargs)

        # Get all items belonging to this order
        context["items"] = self.object.items.all()

        return context


# =========================================================
# ORDER CREATE
# =========================================================

class OrderCreateView(View):

    # Template used for creating an order
    template_name = "orders/order_form.html"

    def get(self, request, *args, **kwargs):

        # Create one empty OrderItem form
        formset = OrderItemFormSet()

        # Get all customers
        customers = Customer.customers.all()

        return render(
            request,
            self.template_name,
            {
                "customers": customers,
                "formset": formset,
            }
        )

    def post(self, request, *args, **kwargs):

        logger.info("Order creation submitted")

        # =====================================================
        # GET ORDER INFORMATION
        # =====================================================

        customer_id = request.POST.get("customer")

        status = request.POST.get("status")


        # Check that customer was selected
        if not customer_id:

            messages.error(
                request,
                "Please select a customer."
            )

            return render(
                request,
                self.template_name,
                {
                    "customers": Customer.customers.all(),
                    "formset": OrderItemFormSet(request.POST),
                }
            )


        # Find customer
        customer = get_object_or_404(
            Customer,
            id=customer_id
        )


        # =====================================================
        # CREATE FORMSET
        # =====================================================

        formset = OrderItemFormSet(
            request.POST
        )


        # =====================================================
        # FORMSET VALIDATION
        # =====================================================

        if formset.is_valid():

            # Dictionary to store requested quantities
            # for each product.
            requested_stock = {}


            # =================================================
            # COLLECT REQUESTED STOCK
            # =================================================

            for form in formset:

                # Skip empty forms
                if not form.cleaned_data:
                    continue


                # Skip deleted forms
                if form.cleaned_data.get("DELETE"):
                    continue


                # Get product
                product = form.cleaned_data.get("product")


                # Get quantity
                quantity = form.cleaned_data.get("quantity")


                # Make sure both values exist
                if not product or not quantity:
                    continue


                # Add quantity for this product
                if product.id in requested_stock:

                    requested_stock[product.id] += quantity

                else:

                    requested_stock[product.id] = quantity


            # =================================================
            # CHECK TOTAL STOCK
            # =================================================

            for product_id, total_requested in requested_stock.items():

                # Get product
                product = get_object_or_404(
                    __import__(
                        "products.models",
                        fromlist=["Product"]
                    ).Product,
                    id=product_id
                )


                # Check total requested quantity
                if total_requested > product.stock:

                    logger.warning(
                        f"Not enough stock for "
                        f"{product.product_name}. "
                        f"Requested: {total_requested}. "
                        f"Available: {product.stock}"
                    )


                    messages.error(
                        request,
                        f"Not enough stock for "
                        f"{product.product_name}. "
                        f"Requested: {total_requested}. "
                        f"Available: {product.stock}."
                    )


                    # Do NOT create the order
                    return render(
                        request,
                        self.template_name,
                        {
                            "customers": Customer.customers.all(),
                            "formset": formset,
                        }
                    )


            # =================================================
            # CREATE ORDER
            # =================================================

            order = Order.objects.create(
                customer=customer,
                status=status
            )


            # Connect formset to order
            formset.instance = order


            # =================================================
            # CREATE ORDER ITEMS
            # =================================================

            items = formset.save(
                commit=False
            )


            for item in items:

                # Store current product price
                item.unit_price = (
                    item.product.product_price
                )


                # Save OrderItem
                item.save()


                # Reduce product stock
                item.product.stock -= item.quantity


                # Save Product
                item.product.save()


            # =================================================
            # SUCCESS
            # =================================================

            logger.info(
                f"Order {order.id} created successfully"
            )


            messages.success(
                request,
                f"Order #{order.id} created successfully."
            )


            return redirect(
                "order_detail",
                id=order.id
            )


        # =====================================================
        # INVALID FORMSET
        # =====================================================

        return render(
            request,
            self.template_name,
            {
                "customers": Customer.customers.all(),
                "formset": formset,
            }
        )


# =========================================================
# ORDER UPDATE
# =========================================================

class OrderUpdateView(View):

    template_name = "orders/order_form.html"

    def get(self, request, id, *args, **kwargs):

        # Get existing order
        order = get_object_or_404(
            Order,
            id=id
        )


        # Get existing order items
        formset = OrderItemFormSet(
            instance=order
        )


        # Get customers
        customers = Customer.customers.all()


        return render(
            request,
            self.template_name,
            {
                "order": order,
                "customers": customers,
                "formset": formset,
            }
        )


    def post(self, request, id, *args, **kwargs):

        # Get existing order
        order = get_object_or_404(
            Order,
            id=id
        )


        # =====================================================
        # UPDATE ORDER INFORMATION
        # =====================================================

        customer_id = request.POST.get("customer")

        status = request.POST.get("status")


        # Find customer
        customer = get_object_or_404(
            Customer,
            id=customer_id
        )


        # Update order
        order.customer = customer

        order.status = status


        # =====================================================
        # UPDATE FORMSET
        # =====================================================

        formset = OrderItemFormSet(
            request.POST,
            instance=order
        )


        # Check formset
        if formset.is_valid():

            # Save items without committing first
            items = formset.save(
                commit=False
            )


            # Update each item
            for item in items:

                # Update price
                item.unit_price = (
                    item.product.product_price
                )

                # Save item
                item.save()


            # Delete items marked for deletion
            for item in formset.deleted_objects:

                item.delete()


            # Save order
            order.save()


            logger.info(
                f"Order {order.id} updated successfully"
            )


            messages.success(
                request,
                f"Order #{order.id} updated successfully."
            )


            return redirect(
                "order_detail",
                id=order.id
            )


        # =====================================================
        # INVALID FORMSET
        # =====================================================

        return render(
            request,
            self.template_name,
            {
                "order": order,
                "customers": Customer.customers.all(),
                "formset": formset,
            }
        )


# =========================================================
# ORDER DELETE
# =========================================================

class OrderDeleteView(DeleteView):

    # Model being deleted
    model = Order

    # Confirmation template
    template_name = "orders/order_confirm_delete.html"

    # URL uses <int:id>
    pk_url_kwarg = "id"

    # Redirect after deletion
    success_url = "/orders/"