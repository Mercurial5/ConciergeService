from typing import Type

from django.db.models import Q
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

    def get_queryset(self):
        current_user = self.request.user
        chats = models.Chat.objects.filter(Q(manager=current_user) | Q(collocutor=current_user)).values('id')
        return self.queryset.filter(id__in=chats)

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


class MessageTypeViewSet(ModelViewSet):
    serializer_class = serializers.MessageTypeSerializer
    permission_classes: list[Type[BasePermission]] = [IsAuthenticated]
    queryset = models.MessageType.objects.all()


class MessageViewSet(ModelViewSet):
    serializer_class = serializers.MessageSerializer
    permission_classes: list[Type[BasePermission]] = [IsAuthenticated]

    def get_queryset(self):
        return models.Message.objects.filter(chat_id=self.kwargs['chat_pk'])
