from rest_framework import serializers
from .models import Participant


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model=Roctaves
        fields=('name','email_address')
        
