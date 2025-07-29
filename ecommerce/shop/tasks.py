# shop/tasks.py
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_order_email(email):
    send_mail(
        subject="Order Confirmation",
        message="Your order has been placed successfully!",
        from_email="admin@ecommerce.com",
        recipient_list=[email],
    )
