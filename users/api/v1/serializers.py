from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import check_password
from django.core.mail import EmailMultiAlternatives
import pyotp
from users.models import OTP
from users.tasks import(
    send_otp,
    send_welcome_mssg
)
from typing import Any
from users.models import OTP

CustomUser = get_user_model()


class UserSerializers(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, required=True, write_only=True)
    email = serializers.EmailField(required=True, write_only=True)

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "password", "email"]

    def create(self, validated_data:dict[str,Any]) -> CustomUser:
       user = CustomUser.objects.create_user(**validated_data)
       send_welcome_mssg(validated_data)
       return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["info"] = f"Thanks for registering with us."
        return data


class SignInSerializer(TokenObtainPairSerializer):
    ...


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, min_length=8, write_only=True)

    class Meta:
        model = CustomUser
        fields = ["password"]

    def validate_password(self, given_password:str) -> str:
        user = self.context["request"].user

        if check_password(given_password, user.password):
            raise serializers.ValidationError(
                {"error-message": "password can't be same as previous password"}
            )
        return given_password

    def update(self, instance, validated_data) -> dict[str,Any]:
        instance.set_password(validated_data["password"])
        instance.save()
        return instance

    def to_representation(self, instance:dict[str,Any]) -> dict[str,Any]:
        data = super().to_representation(instance)
        data["info"] = "Password changed Succesfully"
        return data


class UpdateProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "image", "other_name"]

    def update(self, instance:CustomUser, validated_data:dict[str,Any]) -> CustomUser:
        return super().update(instance, validated_data)

    def to_representation(self, instance:dict[str,Any]) -> dict[str,Any]:
        data = super().to_representation(instance)
        return data


class OtpGenerationSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)

    def validate(self, data:dict[str:Any]) -> dict[str:Any]:
        user = CustomUser.objects.filter(email=data["email"])
        user_otp = OTP.objects.filter(email=data["email"])

        if user.exists() is False:  # Checks if user exists
            raise serializers.ValidationError({"error-message": "User doen't exist."})
        if user_otp.exists(): # Checks if there is an existing otp for the user and deletes it
            user_otp.delete()
        return data

    def create(self, validated_data:dict[str,Any]) -> dict[str:Any]:
        totp = pyotp.TOTP(pyotp.random_base32(), digits=6)
        OTP.objects.create(
                    email=validated_data["email"], 
                    otp=totp.now()
                )
        
        user = CustomUser.objects.get(email=validated_data["email"])
        user.is_active = False
        user.save()
        send_otp(totp.now(), validated_data)
        return validated_data

    def to_representation(self, instance) -> dict[str,Any]:
        data = super().to_representation(instance)
        data["message"] = f"otp has been sent to your email:{data['email']}"
        data.pop("email")
        return data


class OtpVerificationSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(max_length=6, write_only=True)
    class Meta:
        model = OTP
        fields = ["otp", "email"]


    def validate(self, data) -> dict[str,Any]:
        otp_object = OTP.objects.filter(otp=data["otp"], email=data["email"])

        if otp_object.exists():
            return data
        else:
            raise serializers.ValidationError({
                "error-message": "Invalid details given"
            })
        
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password1 = serializers.CharField(min_length=8, write_only=True)
    password2 = serializers.CharField(min_length=8, write_only=True)

    def validate(self, data) -> dict[str,Any]:    
        if CustomUser.objects.filter(email=data["email"]).exists() is False:
            raise serializers.ValidationError({
                "error-mesaage":"Pls recheck the email provided"
            })
                
        elif (data["password1"] != data["password2"]):
            raise serializers.ValidationError({
                "error-message": "Password1 and password2 are not the same"
            })
        
        else:
            user = CustomUser.objects.get(email=data["email"])
            user.set_password(data["password1"])
            user.is_active = True
            user.save()
        return data
    


    




        

        

    

    



