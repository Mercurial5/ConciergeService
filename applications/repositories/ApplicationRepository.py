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

        try:
            owner = self.user_service.get(owner_id)
        except UserDoesNotExist:
            raise exceptions.OwnerDoesNotExist(f'Owner with id {owner_id} does not exist.')

        if owner.role.name not in ('client', 'company'):
            raise exceptions.NotClientOrCompany(f'User with id {owner_id} is not a client or a company.')

        return self.model.objects.create(owner_id=owner_id)

    def get_list(self) -> QuerySet[models.Application]:
        return self.model.objects.all()
