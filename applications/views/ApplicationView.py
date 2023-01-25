from typing import Type

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from applications import serializers, services, exceptions, filters
from users.services import UserService
from users.permissions import IsAdmin


class ApplicationViewSet(ModelViewSet):
    serializer_class = serializers.ApplicationSerializer
    service = services.ApplicationService(UserService())
    permission_classes: list[Type[BasePermission]] = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.ApplicationFilter

    def get_queryset(self):
        user = self.request.user
        queryset = self.service.get_list()

        if self.action == "list" and user.role.name not in ['admin', 'manager']:
            queryset = queryset.filter(owner_id=user.pk)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.ApplicationCreateSerializer
        if self.request.method == 'PATCH':
            return serializers.ApplicationPartiallyUpdateSerializer

        return self.serializer_class

    def get_permissions(self):
        permission_classes = self.permission_classes

        if self.request.method == 'DELETE':
            permission_classes.append(IsAdmin)

        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        request.data['owner'] = self.request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            service = self.service.create(serializer.validated_data)
        except exceptions.ApplicationException as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(service)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
