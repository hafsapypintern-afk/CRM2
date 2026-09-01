
from django import forms
from django.forms import inlineformset_factory

from .models import Order, OrderItem


# =========================================================
# ORDER ITEM FORM
# =========================================================
# This form is used to create/update ONE OrderItem.
# An OrderItem contains:
# - Product
# - Quantity
# We use ModelForm so Django automatically creates
# the form fields from our OrderItem model.
class OrderItemForm(forms.ModelForm):

    class Meta:

        # Tell Django which model this form belongs to
        model = OrderItem

        # Only show these fields in the form
        fields = ["product", "quantity"]


    # =====================================================
    # CUSTOM FORM SETTINGS
    # =====================================================
    def __init__(self, *args, **kwargs):

        # Run Django's normal ModelForm initialization
        # *args  = positional arguments
        # **kwargs = keyword arguments
        # We pass them to the parent ModelForm.
        super().__init__(*args, **kwargs)


        # =====================================================
        # PRODUCT FIELD
        # =====================================================
        # Add Bootstrap CSS classes to the product dropdown.
        self.fields["product"].widget.attrs.update({

            "class": "form-select product-select"
        })


        # =====================================================
        # QUANTITY FIELD
        # =====================================================
        # Add Bootstrap class to the quantity input.
        # min="1" means the browser will not allow
        # a quantity smaller than 1 through normal
        # HTML validation.
        self.fields["quantity"].widget.attrs.update({

            "class": "form-control",

            "min": "1"
        })


    # =====================================================
    # CUSTOM VALIDATION
    # =====================================================
    # clean() is called when Django validates the form.
    # We use it for our business rule:
    #     User cannot order more products
    #     than are currently in stock.
    def clean(self):

        # First let Django perform its normal validation.
        # cleaned_data contains the cleaned values
        # entered/selected by the user.
        cleaned_data = super().clean()

        # Get the selected Product from the form.
        product = cleaned_data.get("product")


        # Get the entered Quantity from the form.
        quantity = cleaned_data.get("quantity")


        # Only perform the stock check if both fields
        # contain valid values.
        if product and quantity:

            # Compare requested quantity with
            # the product's available stock.
            # Example:
            # stock = 2
            # quantity = 5
            # 5 > 2 → True
            if quantity > product.stock:

                # Make the form invalid.
                # Django will show this error to the user
                # instead of allowing the invalid item.
                raise forms.ValidationError(
                    f"Not enough stock for {product.product_name}. "
                    f"Available stock: {product.stock}."
                )


        # Return the cleaned data.
        return cleaned_data


# =========================================================
# ORDER ITEM FORMSET
# =========================================================
# A normal OrderItemForm represents ONE item
# A formset allows us to work with MULTIPLE OrderItems
# together
# Example:
# Order
#   ├── Laptop × 1
#   ├── Mouse × 2
#   └── Keyboard × 1
#
# inlineformset_factory connects Order and OrderItem.
OrderItemFormSet = inlineformset_factory(

    # Parent model
    Order,

    # Child model
    OrderItem,

    # Form to use for each OrderItem
    form=OrderItemForm,

    # Show ONE empty item form initially
    extra=1,

    # Allow existing items to be marked for deletion
    can_delete=True
)

