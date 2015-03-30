from rest_framework import serializers
from social.models import Message, Member

class MemberSerializer(serializers.HyperlinkedModelSerializer):

    receiver_member = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='message-detail'
    )
    sender_member = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='message-detail'
    )
    
    class Meta:
        model = Member
        fields = ('url', 'username', 'password', 'receiver_member', 'sender_member')
        extra_kwargs = {'password': {'write_only': True}}


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Message
        fields = ('url', 'id', 'time', 'message', 'receiver', 'sender', 'is_private')

''' 
class MemberSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=16)
    password = serializers.CharField(max_length=16, write_only=True)
    receiver_member = serializers.HyperlinkedRelatedField(
        many=True, 
        read_only=True, 
        view_name='message-detail'
    )
    sender_member = serializers.HyperlinkedRelatedField(
        many=True, 
        read_only=True, 
        view_name='message-detail'
    )
    
class MessageSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    time = serializers.DateTimeField(read_only=True)
    message = serializers.CharField(max_length=4096)
    receiver = serializers.CharField(max_length=16)
    sender = serializers.CharField(max_length=16)
    is_private = serializers.BooleanField(required=False)
'''     


