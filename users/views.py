from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiExample
# from drf_spectacular.types import OpenApiTypes
from rest_framework import generics, permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken 
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token 
from users.throttle import OtpGenerationThrottle

from users.serializers import (
    UserSerializers,
    SignInSerializer,
    ChangePasswordSerializer,
    UpdateProfileSerializer,
    OtpGenerationSerializer
)

CustomUser = get_user_model()

class CreateUserAPIView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializers
    queryset = CustomUser

    @extend_schema(
        parameters=[
        ],
        request=UserSerializers,
        responses=UserSerializers,
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class SignInAPIView(TokenObtainPairView):
    serializer_class = SignInSerializer
    permission_classes = [permissions.AllowAny]
    
    # @transaction.atomic()
    @extend_schema(
        examples=[
            OpenApiExample(
                "Example",
                response_only=True,
                value={
                    "data": {
                        "acesss-token": "gfevjfuyfuvdhqqwefduyhvwdjhvjhwefkvhfjevjhvjh-qwfuyfhvhqyuviviyv-hfgigiu",
                    },
                },
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class ChangePasswordAPIView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    http_method_names = ["patch"]
    queryset = CustomUser.objects.all()

    def get_object(self):   
        return self.request.user
    
    @extend_schema(
        description= "This endpoint is for changing password",    
        responses= ChangePasswordSerializer,
        examples=[
            OpenApiExample(
                "Example",
                response_only=True,
                value={
                    "data": {
                        "code": 200,
                        "info": "password changes successfully",
                    },
                },
            )
        ]
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

class UpdateProfileAPIView(generics.RetrieveUpdateAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UpdateProfileSerializer
    queryset = CustomUser.objects.all()
    http_method_names = ["put"]

    def get_object(self):
        return self.request.user
    
    @extend_schema(
        examples=[
            OpenApiExample(
                "Example",
                response_only=True,
                value={
                    "data": {
                        "first_name": "string",
                        "last_name": "string",
                        "image": "file.png",
                        "other_name": "string"
                    },
                },
            )
        ]
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class OtpGenerationAPIView(generics.CreateAPIView):
    serializer_class = OtpGenerationSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [OtpGenerationThrottle]

    @extend_schema(
        examples=[
            OpenApiExample(
                "Example",
                response_only=True,
                value={
                    "data": {
                         "message": "otp has been sent to your email:josephfew73@gmail.com",
                    },
                },
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)




    


    
