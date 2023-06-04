from django.urls import path
from mails.views import (
    MailAPIView
)

urlpatterns = [

    path("send-mail/", MailAPIView.as_view(), name="send-mail"),

]