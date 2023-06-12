from rest_framework import serializers
from django.contrib.auth import get_user_model
from drf_spectacular.utils import OpenApiExample
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import validate_email
from django.core.mail import EmailMultiAlternatives
from django_otp.models import Device
import pyotp
from users.models import(
    OTP
)

CustomUser = get_user_model()

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "password", "email"]
        extra_kwargs = {
            "password": {
                "write_only": True
            },
            "email":{
                "required": True
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
    

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "image", "other_name"]

        extra_kwargs = {
            "image": {
                "required" : False
                }
        }   
        
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class OtpGenerationSerializer(serializers.ModelSerializer):
        
        class Meta:
            model = OTP
            fields = ["email"]
        
        def validate(self, attrs):
            provided_email = attrs["email"]
            print(provided_email)

            user = CustomUser.objects.filter(email = provided_email)
            if user.exists() == False:
                raise serializers.ValidationError("Users doen't exist.")
    
            return attrs
                
        def create(self, validated_data):
            totp = pyotp.TOTP(pyotp.random_base32(), digits=6)
            otp = totp.now()  
            print("oooo", otp)

            otp_generation = OTP.objects.create(email=validated_data["email"], otp=otp)

            msg = EmailMultiAlternatives("Below is your otp", f"YOUR OTP is {otp}, mustn't be shared with anyone.",
                             "josephmiracle119@gmail.com", [validated_data["email"]])
            msg.send()
            
            return validated_data
        
        def to_representation(self, instance):
            data = super().to_representation(instance)
            data["message"] = f"otp has been sent to your email:{data['email']}"
            data.pop('email')
            
            return data

                

