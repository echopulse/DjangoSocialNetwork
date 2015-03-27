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
        fields = ('username', 'password', 'receiver_member', 'sender_member')
        extra_kwargs = {'password': {'write_only': True}}


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Message
        fields = ('id', 'time', 'message', 'receiver', 'sender', 'is_private')

 
#class MemberSerializer(serializers.Serializer):
#    username = serializers.CharField(max_length=16)
    
#class MessageSerializer(serializers.Serializer):
#    sender = MemberSerializer()
#    receiver = MemberSerializer()
#    message = serializers.CharField(max_length=4096)
#    time = serializers.DateTimeField()       
