from django.urls import path
from users.views import (
    CreateUserAPIView,
    SignInAPIView
)


urlpatterns =[
    path("signup/", CreateUserAPIView.as_view(), name="signup"),  
    path("signin/", SignInAPIView.as_view(), name="signin"),
]