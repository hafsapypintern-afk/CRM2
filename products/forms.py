from django import forms
from .models import Product

class ProductForm(forms.ModelForm):


    class Meta:
        model = Product

        fields = [
            "product_name",
            "product_description",
            "product_price",
            "stock",
        ]

        widgets = {

            "product_name": forms.TextInput(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Enter product name",
                }
            ),

            "product_description": forms.Textarea(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Enter product description",
                    "rows": 5,
                }
            ),

            "product_price": forms.NumberInput(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Enter product price",
                    "step": "1",
                    "min": "0",
                }
            ),

            "stock": forms.NumberInput(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "Enter stock quantity",
                    "min": "0",
                }
            ),
        }