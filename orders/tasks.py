from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .models import Order


@shared_task
def send_order_created_email(order_id):

    order = Order.objects.get(id=order_id)

    customer = order.customer
    items = order.items.all()

    item_lines = []
    total = 0

    for item in items:

        item_total = item.quantity * item.unit_price
        total += item_total

        item_lines.append(
            f"- {item.product.product_name} "
            f"x {item.quantity} — Rs. {item_total}"
        )

    items_text = "\n".join(item_lines)

    send_mail(
        subject=f"New Order Created — Order #{order.id}",
        message=(
            f"A new order has been created.\n\n"
            f"Customer: "
            f"{customer.first_name} {customer.last_name}\n"
            f"Email: {customer.email}\n\n"
            f"Order #{order.id}\n"
            f"Status: {order.status}\n\n"
            f"Items:\n"
            f"{items_text}\n\n"
            f"Total: Rs. {total}"
        ),
        from_email=None,
        recipient_list=[settings.ADMIN_EMAIL],
    )

    return f"Order creation email sent for order #{order.id}"


@shared_task
def send_order_updated_email(order_id):

    order = Order.objects.get(id=order_id)

    customer = order.customer
    items = order.items.all()

    item_lines = []
    total = 0

    for item in items:

        item_total = item.quantity * item.unit_price
        total += item_total

        item_lines.append(
            f"- {item.product.product_name} "
            f"x {item.quantity} — Rs. {item_total}"
        )

    items_text = "\n".join(item_lines)

    send_mail(
        subject=f"Order Updated — Order #{order.id}",
        message=(
            f"An order has been updated.\n\n"
            f"Customer: "
            f"{customer.first_name} {customer.last_name}\n"
            f"Email: {customer.email}\n\n"
            f"Order #{order.id}\n"
            f"Status: {order.status}\n\n"
            f"Updated Items:\n"
            f"{items_text}\n\n"
            f"Total: Rs. {total}"
        ),
        from_email=None,
        recipient_list=[settings.ADMIN_EMAIL],
    )

    return f"Order update email sent for order #{order.id}"



@shared_task
def send_order_deleted_email(
    order_id,
    customer_name,
    customer_email,
    status,
    items_text,
    total,
):

    send_mail(
        subject=f"Order Deleted — Order #{order_id}",
        message=(
            f"An order has been deleted from the CRM.\n\n"
            f"Customer: {customer_name}\n"
            f"Email: {customer_email}\n\n"
            f"Order #{order_id}\n"
            f"Status: {status}\n\n"
            f"Deleted Items:\n"
            f"{items_text}\n\n"
            f"Total: Rs. {total}"
        ),
        from_email=None,
        recipient_list=[settings.ADMIN_EMAIL],
    )

    return f"Order deletion email sent for order #{order_id}"