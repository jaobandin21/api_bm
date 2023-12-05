from rest_framework import (
    viewsets,
    status
)
# from django.db import transaction
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from account import serializers
# from utils.generated_code import GenerateCode
from core import models as core_model
# import datetime
# import base64
# import io
# from django.core.files.base import File
# from django.utils import timezone


class AccountView(viewsets.ModelViewSet):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(methods=['GET'], detail=True)
    def account_detailed(self, request, pk=None):
        """
            url:/api/account/<user_id>/account_detailed/
        """

        account = core_model.Account.objects.filter(
            user__id=pk
        ).first()

        if not account:
            return Response(
                "Account not found!",
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            "success": True,
            "data": serializers.AccountSerializer(
                instance=account,
                many=False
            ).data,
        }, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def account_list(self, request, pk=None):
        """
           url:/api/account/account_list/?client_id=1
        """
        client_id = int(request.query_params.get("client_id"))

        client = core_model.Client.objects.filter(id=client_id).first()

        if not client:
            return Response(
                "Client not found!",
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            "success": True,
            "data": serializers.AccountSerializer(
                instance=core_model.Account.objects.filter(
                    client=client
                ).exclude(status=core_model.Account.DELETED),
                many=True
            ).data,
        }, status=status.HTTP_200_OK)
