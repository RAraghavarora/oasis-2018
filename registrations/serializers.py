from rest_framework import serializers

from registrations.models import *

class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = '__all__'

class IntroRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntroReg
        fields = '__all__'
