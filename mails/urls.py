from django.urls import path
from mails.views import (
    MailAPIView,
    GetSentMailAPIView
)

urlpatterns = [

    path("send-mail/", MailAPIView.as_view(), name="send-mail"),
    path("get/", GetSentMailAPIView.as_view(), name="get"),

]