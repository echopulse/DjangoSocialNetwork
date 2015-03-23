from rest_framework import serializers
from social.models import Message

class MessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Message
        fields = ('id', 'time', 'message', 'receiver', 'sender', 'is_private')


