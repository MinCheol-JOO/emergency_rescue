from rest_framework import serializers
from .models import * 

class Emergency_RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emergency_Room
        fields = ('__all__')
