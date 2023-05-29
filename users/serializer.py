from rest_framework import serializers
from django.contrib.auth import get_user_model
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import check_password

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

class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["password"]

        extra_kwargs = {
            'password': {
                'write_only': True
                },
        }

    def validate_password(self, given_password):
        user = self.context['request'].user
        
        if len(given_password) < 8:
            raise serializers.ValidationError("Password is short")
        
        elif check_password(given_password, user.password):
            raise serializers.ValidationError("password can't be same as previous password")
        return given_password
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance
    
    def to_representation(self, instance):
        data = super().to_representation(instance)     
        data["info"] = "Password changed Succesfully"
        return data
        
