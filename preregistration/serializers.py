from rest_framework import serializers
from .models import Participant


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model=Participant
        fields=('name','phone','email_address','city')
        
