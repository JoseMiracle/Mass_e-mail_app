from django.urls import path
from users.api.v1.views import (
    CreateUserAPIView,
    SignInAPIView,
    ChangePasswordAPIView,
    UpdateProfileAPIView,
    OtpGenerationAPIView,
    OtpVerificationAPIView,
    ResetPasswordAPIView,
)


urlpatterns = [
    path("sign-up/", CreateUserAPIView.as_view(), name="sign-up"),
    path("sign-in/", SignInAPIView.as_view(), name="sign-in"),
    path("change-password/", ChangePasswordAPIView.as_view(), name="change-password"),
    path("update-profile/", UpdateProfileAPIView.as_view(), name="update-profile"),
    path("otp-generation/", OtpGenerationAPIView.as_view(), name="reset-password"),
    path(
        "otp-verification/", OtpVerificationAPIView.as_view(), name="otp-verification"
    ),
    path("reset-password/", ResetPasswordAPIView.as_view(), name="reset-password"),
]
