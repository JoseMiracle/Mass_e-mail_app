from rest_framework import serializers
from django.core.mail import EmailMultiAlternatives
from anymail.message import attach_inline_image_file

from users.models import(
    CustomUser
)
from users.serializers import(
    UserSerializers
)
from mails.models import (
    Mail
)

class SendMailSerializer(serializers.ModelSerializer): # This is for serializing mails sent by user
    sender = UserSerializers(required= False) 
    receiver = serializers.ListField(child=serializers.EmailField())

    class Meta:
        model = Mail
        fields = ["sender", "receiver"]
        extra_kwargs = {
            "receiver": {
                "required": True,
            },
            "sender":{
                "read_only": True,
            }
        }

    def create(self, validated_data):
        mail_receivers = validated_data.pop('receiver')
        receivers = []
        
        for mail_receiver in mail_receivers:
            mail_obj = Mail.objects.create(sender=self.context['request'].user, receiver=mail_receiver)
            receivers.append(mail_receiver)
            
        if len(receivers) > 0:
            msg = EmailMultiAlternatives( 
                    subject="Please activate your account",
                    body="Click to activate your account: https://example.com/activate",
                    from_email="josephmiracle119@gmail.com",
                    to=[receiver for receiver in receivers],
                    reply_to=["josephmiracle119@gmail.com"]
            )
            msg.send()

        return {
            "receiver": mail_receivers
        }
    
    def to_representation(self, instance):
        data =  super().to_representation(instance)
        data["sender"] = self.context['request'].user.email

        return data
    
class AllMailSerializer(serializers.ModelSerializer): # This is for fetching sent and unsent mail by user
    sender = UserSerializers()
    
    class Meta:
        model = Mail
        fields = ["sender", "receiver"]



