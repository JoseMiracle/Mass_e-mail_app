from django.core.mail import EmailMultiAlternatives
from celery import shared_task


@shared_task
def send_mass_mail(subject, body, from_email, receivers, reply_to):
    """This sends mail to multiple users"""

    msg = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=from_email,
        to=receivers,
        reply_to=[reply_to],
    )
    msg.send()
