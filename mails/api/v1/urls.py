from django.urls import path
from mails.api.v1.views import SendMailAPIView, GetSentMailAPIView

urlpatterns = [
    path("send-mails/", SendMailAPIView.as_view(), name="send-mails"),
    path("get-sent-mails/", GetSentMailAPIView.as_view(), name="get-sent-mails"),
]
