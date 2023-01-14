from __future__ import annotations
from typing import Protocol, OrderedDict

from django.db.models import QuerySet

from applications import models, exceptions
from users.exceptions import UserDoesNotExist
from users.services import UserServiceInterface


class ApplicationRepositoryInterface(Protocol):
    def create(self, data: OrderedDict) -> models.Application: ...

    def get_list(self) -> QuerySet[models.Application]: ...


class ApplicationRepository:
    model = models.Application

    def __init__(self, user_service: UserServiceInterface):
        self.user_service = user_service

    def create(self, data: OrderedDict) -> models.Application:
        owner_id = data['owner_id']

        services_data = data['services']
        del data['services']

        try:
            owner = self.user_service.get(owner_id)
        except UserDoesNotExist:
            raise exceptions.OwnerDoesNotExist(f'Owner with id {owner_id} does not exist.')

        if owner.role.name not in ('client', 'company'):
            raise exceptions.NotClientOrCompany(f'User with id {owner_id} is not a client or a company.')

        if len(services_data) < 1:
            raise exceptions.NoServices('Application should have 1 or more services.')

        application = self.model.objects.create(**data)
        for service in services_data:
            application.services.create(**service)

        return application

    def get_list(self) -> QuerySet[models.Application]:
        return self.model.objects.all()
