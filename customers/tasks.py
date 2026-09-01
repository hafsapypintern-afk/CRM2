from celery import shared_task
from django.core.mail import send_mail


@shared_task
def test_task():
    return "Celery is working!"


@shared_task
def send_customer_email(customer_name, customer_email):
    send_mail(
        subject="Welcome to CRM",
        message=f"Hello {customer_name}, welcome to our CRM!",
        from_email=None,
        recipient_list=[customer_email],
    )

    return f"Email sent to {customer_email}"
