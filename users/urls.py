from django.urls import path
from users.views import (
    CreateUserApi
)


urlpatterns =[
    path("signup/", CreateUserApi.as_view(), name="signup"),  
]