from rest_framework import serializers
from preregistration.models import *

#this is for Roctaves Participants
class RoctavesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Roctaves
        fields=('name','email_address')

class GenPartcipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenParticipant
        fields=('name','phone','email_address','city','gender')

class PoetrySlamSerializer(serializers.ModelSerializer):
    name = serializers.RelatedField(source='GenParticipant', read_only=True)
    phone = serializers.RelatedField(source='GenParticipant', read_only=True)
    email_address = serializers.RelatedField(source='GenParticipant', read_only=True)
    city = serializers.RelatedField(source='GenParticipant', read_only=True)

    class Meta:
        model = PoetrySlamExtension
        fields = ('name', 'phone', 'email_address', 'city')

class RapWarsSerializer(serializers.ModelSerializer):
    name = serializers.RelatedField(source='GenParticipant', read_only=True)
    phone = serializers.RelatedField(source='GenParticipant', read_only=True)
    email_address = serializers.RelatedField(source='GenParticipant', read_only=True)
    city = serializers.RelatedField(source='GenParticipant', read_only=True)

    class Meta:
        model = RapWarsExtension
        fields = ('name', 'rapper_name', 'phone','email_address', 'city', 'city_of_participation')

#serializers changed
