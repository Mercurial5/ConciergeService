from typing import Type

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from chat import serializers, models
from users.permissions import IsManager


class ChatViewSet(ModelViewSet):
    serializer_class = serializers.ChatSerializer
    queryset = models.Chat.objects.all()
    permission_classes: list[Type[BasePermission]] = [IsAuthenticated]

    def get_permissions(self):
        permission_classes = self.permission_classes

        if self.request.method == 'POST':
            permission_classes.append(IsManager)

        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        request.data['manager'] = self.request.user.id

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        models.Chat.objects.create(**serializer.validated_data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
