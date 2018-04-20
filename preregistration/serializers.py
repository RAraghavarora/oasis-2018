from rest_framework import serializers
from .models import Roctaves


class RoctaveSerializer(serializers.ModelSerializer):
    class Meta:
        model=Roctaves
        fields=('name','phone','email_address')
        