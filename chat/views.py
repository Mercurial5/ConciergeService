from typing import Type

from django.db.models import Q
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from chat import serializers, models
from users.permissions import IsManager


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ChatViewSet(ModelViewSet):
    serializer_class = serializers.ChatSerializer
    queryset = models.Chat.objects.all()
    permission_classes: list[Type[BasePermission]] = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        current_user = self.request.user
        chats = models.Chat.objects.filter(Q(manager=current_user) | Q(collocutor=current_user)).values('id')
        return self.queryset.filter(id__in=chats)

    def get_permissions(self):
        permission_classes = self.permission_classes

        if self.request.method == 'POST':
            permission_classes.append(IsManager)

        return [permission() for permission in permission_classes]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.collocutor = instance.collocutor if instance.manager.id == request.user.id else instance.manager
        serializer = serializers.ChatReadSerializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        for chat in queryset:
            chat.collocutor = chat.collocutor if chat.manager.id == request.user.id else chat.manager

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.ChatReadSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.ChatReadSerializer(queryset, many=True)
        return Response(serializer.data)

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
