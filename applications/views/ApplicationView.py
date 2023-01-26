from typing import Type

from django_filters.rest_framework import DjangoFilterBackend
from djoser.compat import get_user_email
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from applications import serializers, services, exceptions, filters
from users.models import User
from users.permissions import IsAdmin, IsManager
from users.services import UserService
from users import email

from chat import models


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

    @action(methods=['GET'], detail=True, permission_classes=[IsManager])
    def take(self, request, pk: int, *args, **kwargs):
        try:
            application = self.service.get(pk)
        except models.Application.DoesNotExist as e:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if application.manager is not None:
            return Response({'detail': 'This application already have been taken'}, status=status.HTTP_400_BAD_REQUEST)

        application.manager_id = self.request.user.id
        application.status_id = 2
        application.save(update_fields=['manager_id', 'status_id'])

        owner: User = application.owner
        if not owner.is_active:
            user_service = UserService()
            password = user_service.set_password(owner)
            user_service.activate(owner)

            context = {'user': owner, 'password': password}
            to = [get_user_email(owner)]

            email.ActivationEmail(self.request, context).send(to)

        chat = models.Chat.objects.create(application=application, manager=self.request.user, collocutor=owner)

        starred_type = models.MessageType.objects.get(name='starred')
        for service in application.services.all():
            msg = f'Категория: {service.category.name}\n\n'

            if service.date_from:
                msg += f'С: {service.date_from}\n'
            if service.date_to:
                msg += f'До: {service.date_to}\n'

            msg += f'\n{service.description}'
            chat.message_set.create(sender=owner, type=starred_type, content=msg)

        return Response({}, status=status.HTTP_200_OK)
