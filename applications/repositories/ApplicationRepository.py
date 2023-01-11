from typing import Protocol

from django.db.models import QuerySet

from applications import models, exceptions
from users.exceptions import UserDoesNotExist
from users.services import UserServiceInterface


class ApplicationRepositoryInterface(Protocol):
    def create(self, **kwargs) -> models.Application: ...

    def get_list(self) -> QuerySet[models.Application]: ...


class ApplicationRepository:
    model = models.Application

    def __init__(self, user_service: UserServiceInterface):
        self.user_service = user_service

    def create(self, **kwargs) -> models.Application:
        owner_id = kwargs['owner_id']
        manager_id = kwargs['manager_id']

        try:
            owner = self.user_service.get(owner_id)
        except UserDoesNotExist:
            raise exceptions.OwnerDoesNotExist(f'Owner with id {owner_id} does not exist.')

        if owner.role.name not in ('client', 'company'):
            raise exceptions.NotClientOrCompany(f'User with id {owner_id} is not a client or a company.')

        try:
            manager = self.user_service.get(manager_id)
        except UserDoesNotExist:
            raise exceptions.ManagerDoesNotExist(f'Manager with id {manager_id} does not exist.')

        if manager.role.name != 'manager':
            raise exceptions.NotManager(f'User with id {manager_id} is not a manager')

        return self.model.objects.create(**kwargs)

    def get_list(self) -> QuerySet[models.Application]:
        return self.model.objects.all()
