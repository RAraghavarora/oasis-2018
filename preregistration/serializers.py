from rest_framework import serializers
from .models import *

#this is for Roctaves Participants
class RoctavesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Roctaves
        fields=('name','email_address')

class GenPartcipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenParticipant
        fields=('name','phone','email_address','city','gender')

"""
class PoetrySlamSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoetrySlam
        fields = ('name', 'phone', 'email_address', 'city')

class RapWarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RapWars
        fields = ('name', 'rapper_name', 'phone','email_address', 'city', 'city_of_participation')
"""
