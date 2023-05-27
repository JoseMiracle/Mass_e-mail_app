from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model

from users.serializer import (
    UserSerializers
)

CustomUser = get_user_model()

class CreateUserApi(generics.CreateAPIView):
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



