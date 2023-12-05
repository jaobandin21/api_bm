from rest_framework import (
    viewsets,
    status
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core import models as core_models
from . import serializers as client_serializer


class ClientView(viewsets.ModelViewSet):
    serializer_class = client_serializer.ClientSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """url:/api/assessment/"""
        return core_models.Client.objects.all()

    @action(methods=['GET'], detail=True)
    def client_assessment(self, request, pk=None):
        """
            /client/1/client_assessment/
        """
        client_assessment = core_models.ClientAssessment.objects.filter(
            client__id=pk
        )

        return Response({
            "success": True,
            "data": client_serializer.ClientAssessmentSerializer(
                instance=client_assessment,
                many=True
            ).data,
        }, status=status.HTTP_200_OK)
