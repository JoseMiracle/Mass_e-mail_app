from django.shortcuts import render
from rest_framework import generics, permissions, status
from mails.api.v1.serializers import (
    SendMailSerializer,
    GetSentMailSerializer,
)
from mails.models import Mail


class SendMailAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SendMailSerializer
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class GetSentMailAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GetSentMailSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        return Mail.objects.all().filter(sender=self.request.user)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
