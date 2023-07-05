from rest_framework.throttling import AnonRateThrottle


class OtpGenerationThrottle(AnonRateThrottle):
    rate = "1/m"
