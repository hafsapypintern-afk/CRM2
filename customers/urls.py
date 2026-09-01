from django.urls import path
from . import views


urlpatterns = [

    # ========================================================
    # CUSTOMER LIST
    # ========================================================

    path(
        "",
        views.CustomerListView.as_view(),
        name="customer_list"
    ),


    # ========================================================
    # CUSTOMER CREATE
    # ========================================================

    path(
        "create/",
        views.CustomerCreateView.as_view(),
        name="customer_create"
    ),


    # ========================================================
    # CUSTOMER DETAIL
    # ========================================================

    path(
        "<int:pk>/",
        views.CustomerDetailView.as_view(),
        name="customer_detail"
    ),


    # ========================================================
    # CUSTOMER UPDATE
    # ========================================================

    path(
        "<int:pk>/update/",
        views.CustomerUpdateView.as_view(),
        name="customer_update"
    ),


    # ========================================================
    # CUSTOMER DELETE
    # ========================================================

    path(
        "<int:pk>/delete/",
        views.CustomerDeleteView.as_view(),
        name="customer_delete"
    ),
]
