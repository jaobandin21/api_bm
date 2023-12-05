from rest_framework import serializers
from core import models


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Client
        fields = "__all__"
