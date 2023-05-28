from rest_framework import serializers
from django.contrib.auth import get_user_model
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

CustomUser = get_user_model()

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name", "surname", "password", "email"]
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class SignInSerializer(TokenObtainPairSerializer):
    ...