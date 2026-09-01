from django.db import models

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200)
    product_description = models.TextField()
    product_price = models.DecimalField( max_digits=10,decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
     return f"{self.product_name} - Stock: {self.stock}"

