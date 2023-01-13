from __future__ import annotations
from typing import Protocol, OrderedDict, TYPE_CHECKING

from django.db.models import QuerySet

from applications import models, exceptions
from users.exceptions import UserDoesNotExist
from users.services import UserServiceInterface

if TYPE_CHECKING:
    from applications import services


class ApplicationRepositoryInterface(Protocol):
    def create(self, data: OrderedDict) -> models.Application: ...

    def get_list(self) -> QuerySet[models.Application]: ...


class ApplicationRepository:
    model = models.Application

    def __init__(self, user_service: UserServiceInterface, service_service: services.ServiceServiceInterface):
        self.user_service = user_service
        self.service_service = service_service

    def create(self, data: OrderedDict) -> models.Application:
        owner_id = data['owner_id']

        try:
            owner = self.user_service.get(owner_id)
        except UserDoesNotExist:
            raise exceptions.OwnerDoesNotExist(f'Owner with id {owner_id} does not exist.')

        if owner.role.name not in ('client', 'company'):
            raise exceptions.NotClientOrCompany(f'User with id {owner_id} is not a client or a company.')

        application = self.model.objects.create(owner_id=owner_id)

        for service in data['services']:
            application.services.add(self.service_service.create(service))

        return application

    def get_list(self) -> QuerySet[models.Application]:
        return self.model.objects.all()
