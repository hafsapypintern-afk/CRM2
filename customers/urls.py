
from django.urls import path
from . import views

urlpatterns = [
    path("", views.customer_list, name="customer_list"),

    path("create/", views.customer_create, name="customer_create"),

    path("<int:id>/", views.customer_detail, name="customer_detail"),

    path("<int:id>/update/", views.customer_update, name="customer_update"),

    path("<int:id>/delete/", views.customer_delete, name="customer_delete"),
]