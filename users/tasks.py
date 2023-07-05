from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from typing import Any


@shared_task
def send_otp(otp: int, validated_data: dict[str:Any]) -> None:
    """This is for sending otp to user for retrieving account after forgetting password"""
    msg = EmailMultiAlternatives(
        subject="OTP FOR CHANGING PASSWORD",
        body=f"OTP:{otp}, Please do not share with anyone",
        from_email="josephmiracle119@gmail.com",
        to=[validated_data["email"]],
    )
    msg.send()


@shared_task
def send_welcome_mssg(validated_data: dict[str, Any]) -> None:
    """This is for sending welcome message to user after registration"""
    msg = EmailMultiAlternatives(
        subject="Acknowledge Of Registration",
        body="Thank you for signing up with us",
        from_email="josephmiracle119@gmail.com",
        to=[validated_data["email"]],
    )
    msg.send()
