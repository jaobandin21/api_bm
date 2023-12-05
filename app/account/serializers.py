from rest_framework import serializers
from core import models as core_model
from user import serializers as user_serializer
from client import serializers as client_serializer
# from datetime import datetime


class AccountSerializer(serializers.ModelSerializer):
    """Serializer for Account"""
    user = user_serializer.UserSerializer()
    client = client_serializer.ClientSerializer()

    class Meta:
        model = core_model.Account
        fields = [
            'id',
            'client',
            'user',
            'phone_number',
            'mobile_number',
            'user_type',
            'status',
        ]
