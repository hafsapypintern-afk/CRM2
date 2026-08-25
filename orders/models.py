from django.db import models
from django.db import models
from customers.models import Customer
from products.models import Product

# Create your models here.
class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name="orders")
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Order #{self.id} - {self.customer}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="order_items")
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"{self.product} x {self.quantity}"