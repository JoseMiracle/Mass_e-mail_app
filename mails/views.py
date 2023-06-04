from django.shortcuts import render
from rest_framework import generics, permissions, status
from users.models import(
    CustomUser
)
from mails.serializers import(
    MailSerializer
)

class MailAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MailSerializer
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    