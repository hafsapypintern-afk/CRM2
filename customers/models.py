from django.db import models


# ============================================================
# CUSTOM EMAIL FIELD
# ============================================================

# We are creating OUR OWN email field.
# It is based on Django's existing EmailField.
# This is called inheritance.
# Because we inherit from EmailField, we still get
# Django's built-in email validation.
class CustomerEmailField(models.EmailField):

    # __init__ runs when we create CustomerEmailField()
    # *args collects positional arguments.
    # **kwargs collects named arguments such as
    # max_length, blank, null, etc.
    def __init__(self, *args, **kwargs):

        # Our custom email field always has a maximum
        # length of 100 characters.
        kwargs["max_length"] = 100

        # Call the parent EmailField.
        # This allows Django's EmailField to perform
        # its normal work and validation.
        super().__init__(
            *args,
            **kwargs
        )


# ============================================================
# CUSTOMER MODEL
# ============================================================

# Customer model represents a customer in our CRM.
class Customer(models.Model):

    # Customer's first name.
    first_name = models.CharField(
        max_length=100
    )

    # Customer's last name.
    last_name = models.CharField(
        max_length=100
    )

    # Customer's email address.
    #
    # We are using our CUSTOM email field here.
    #
    # It automatically gets:
    # - Django's EmailField validation
    # - max_length = 100
    email = CustomerEmailField()

    # Customer's phone number.
    #
    # This is now a normal CharField.
    phone_number = models.CharField(
        max_length=15
    )

    # Customer's complete address.
    address = models.TextField()

    # Customer's city.
    city = models.CharField(
        max_length=100
    )

    # Automatically stores the date and time when
    # the customer is first created.
    # auto_now_add=True means this value is set
    # when the object is created.
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # Custom manager.
    # This allows us to use:
    # Customer.customers.all()
    # Customer.customers.create()
    # Customer.customers.get()
    # instead of:
    # Customer.objects.all()
    customers = models.Manager()

    # __str__ controls how the Customer object is displayed
    # in Django admin, shell, etc.
    def __str__(self):

        return f"{self.first_name} {self.last_name}"
