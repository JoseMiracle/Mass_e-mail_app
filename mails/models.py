from django.db import models
from users.models import CustomUser
from django.utils.timezone import timedelta


class Mail(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    receiver = models.EmailField(blank=False, null=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Message sent by {self.sender} to {self.receiver}"
