from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiExample
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from users.api.v1.throttle import OtpGenerationThrottle
from rest_framework.views import APIView
from rest_framework.response import Response
from users.api.v1.serializers import (
    UserSerializers,
    SignInSerializer,
    ChangePasswordSerializer,
    UpdateProfileSerializer,
    OtpGenerationSerializer,
    OtpVerificationSerializer,
    ResetPasswordSerializer,
)
from users.models import OTP

CustomUser = get_user_model()

class CreateUserAPIView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializers
    http_method_names = ["post"]

    @extend_schema(
        description= "This endpoint is for creating user",
        examples=[
            OpenApiExample(
                "Example",
                response_only=True,
                value={
                    "data": {
                        "first_name": "John",
                        "last_name": "Doe",
                        "info": "Thanks for registering with us."                    },
                },
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class SignInAPIView(TokenObtainPairView):
    serializer_class = SignInSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ["post"]
    
 
    @extend_schema(
        description= "This endpoint is for signing in",
        examples=[
            OpenApiExample(
                "Example",
                response_only=True,
                value={
                    "data": {
                        "acesss-token": "gfevjfuyfuvdhqqwefduyhvwdjhvjhwefkvhfjevjhvjh-qwfuyfhvhqyuviviyv-hfgigiu",
                        "refresh-token": "gfevjfuyfuvdhqqwefduyhvwdjhvjhwefkvhfjevjhvjh-qwfuyfhvhqyuviviyv-hfgigiu"
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

    def get_object(self):   
        return self.request.user
    
    @extend_schema(
        description= "This endpoint is for changing password",    
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
    http_method_names = ["post"]

    @extend_schema(
        description= "This endpoint is for generating otp",
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


class OtpVerificationAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    http_method_names = ["post"]
    
    @extend_schema(
        description= "This endpoint is for otp verification",
        examples=[
            OpenApiExample(
                "Example",
                response_only=True,
                value={
                    "data": {
                         "message": "OTP Verification Done",
                    },
                },
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        serializer = OtpVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        delete_otp_object = OTP.objects.get(
                email=serializer.validated_data["email"]
            ).delete()
        return Response({
            "info": "OTP Verification Done"
        })
    
class ResetPasswordAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    http_method_names = ["post"]

    @extend_schema(
        description= "This endpoint is for resetting password",
        examples=[
            OpenApiExample(
                "Example",
                response_only=True,
                value={
                    "data": {
                         "message": "Password Reset is Successful",
                    },
                },
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({
            "info": "Password Reset is Successful"
        })
    
    
