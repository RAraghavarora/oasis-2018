#---Imports---#
#Django Imports
from rest_framework import serializers
#Self Imports
from registrations.models import *
#---End of Imports---#

#---Serializers---#
class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = '__all__'

class IntroRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntroReg
        fields = '__all__'
