from rest_framework import serializers
from .models import Roctaves, GenParticipant

#this is for Roctaves Participants
class RoctavesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Roctaves
        fields=('name','email_address')

class GenPartcipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenParticipant
        fields=('name','phone','email_address','city','gender')
