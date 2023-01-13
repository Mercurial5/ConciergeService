from typing import Type

from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.viewsets import GenericViewSet

from applications import serializers, services


class ServiceViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                     mixins.ListModelMixin, GenericViewSet):
    serializer_class = serializers.ServiceSerializer
    service = services.ServiceService()
    permission_classes: list[Type[BasePermission]] = [IsAuthenticated]

    def get_queryset(self):
        return self.service.get_list()
