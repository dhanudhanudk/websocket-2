from rest_framework import serializers
from.models import *



class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['room_name','send_user', 'receiv_user', 'created_at','updated_on']