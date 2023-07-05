from rest_framework import serializers
from mails.models import Mail
from mails.tasks import send_mass_mail


class SendMailSerializer(
    serializers.ModelSerializer
):  # This is for serializing mails sent by user
    receiver = serializers.ListField(child=serializers.EmailField(), required=True)

    class Meta:
        model = Mail
        fields = ["receiver"]

    def create(self, validated_data):
        mail_receivers = validated_data.pop("receiver")
        receivers = []

        for mail_receiver in mail_receivers:
            mail_obj = Mail.objects.create(
                sender=self.context["request"].user, receiver=mail_receiver
            )
            receivers.append(mail_receiver)

        if len(receivers) > 0:
            send_mass_mail(
                subject="Important Information",
                body="Do good to people",
                from_email="josephmiracle119@gmail.com",
                receivers=receivers,
                reply_to="josephmiracle119@gmail.com",
            )
        return {"receiver": mail_receivers}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["sender"] = self.context["request"].user.email
        return data


class GetSentMailSerializer(
    serializers.ModelSerializer
):  # This is for fetching sent and unsent mail by user
    class Meta:
        model = Mail
        fields = ["sender", "receiver", "created_at"]
