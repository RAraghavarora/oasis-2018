from rest_framework import serializers
from .models import Roctaves


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model=Roctaves
        fields=('name','email_address')
        
