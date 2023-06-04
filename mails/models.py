from django.db import models
from users.models import(
    CustomUser
)

class Mail(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    receiver = models.EmailField(blank=False, null=False)

    def __str__(self):
        return f"Message sent by {self.sender} to {self.receiver}"
    

