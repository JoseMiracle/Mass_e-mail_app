from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiExample
# from drf_spectacular.types import OpenApiTypes
from rest_framework import generics, permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from users.serializer import (
    UserSerializers,
    SignInSerializer
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
        response = super().post(request, *args, **kwargs)
        serializer = self.get_serializer(data = request.data)
        data = {

            'access-token' : response.data['access']
        }
        return Response(data, status=status.HTTP_200_OK)


    
