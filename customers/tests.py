from django.test import TestCase
from .models import Customer


class CustomerTest(TestCase):

    def test_customer_manager(self):
        customer = Customer.customers.create(
            first_name="Ali",
            last_name="Khan",
            email="ali@test.com",
            phone_number="03001234567",
            address="Lahore",
            city="Lahore"
        )

        self.assertEqual(customer.first_name, "Ali")