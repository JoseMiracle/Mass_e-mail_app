from django.shortcuts import render
from rest_framework import generics, permissions, status
from users.models import(
    CustomUser
)
from mails.serializers import(
    SendMailSerializer,
    AllMailSerializer,
)
from mails.models import(
    Mail
)

class MailAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SendMailSerializer
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
class GetSentMailAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AllMailSerializer
    queryset = Mail.objects.all()


    def get_queryset(self):
        return Mail.objects.all().filter(sender=self.request.user)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    

