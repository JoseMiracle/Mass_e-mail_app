from django.urls import path
from users.views import (
    CreateUserAPIView,
    SignInAPIView,
    ChangePasswordAPIView
)


urlpatterns =[
    path("signup/", CreateUserAPIView.as_view(), name="signup"),  
    path("signin/", SignInAPIView.as_view(), name="signin"),
    path("change-password/", ChangePasswordAPIView.as_view(), name="change-password"),
]