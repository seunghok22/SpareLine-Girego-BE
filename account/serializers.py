from rest_framework import serializers
from .models import account

class accountSerializer(serializers.ModelSerializer):
    class Meta:
        model = account
        fields = ( 'email')
    def create(self, validated_data):
        account = account(**validated_data)
        account.save()
        return account