from __future__ import annotations
from typing import Protocol, OrderedDict

from django.db.models import QuerySet

from applications import models
from applications.repositories import ApplicationRepositoryInterface, ApplicationRepository
from users.services import UserServiceInterface


class ApplicationServiceInterface(Protocol):
    repo: ApplicationRepositoryInterface

    def create(self, data: OrderedDict) -> models.Application: ...

    def get_list(self) -> QuerySet[models.Application]: ...

    def get(self, pk: int) -> models.Application: ...


class ApplicationService:

    def __init__(self, user_service: UserServiceInterface):
        self.repo: ApplicationRepositoryInterface = ApplicationRepository(user_service)

    def create(self, data: OrderedDict) -> models.Application:
        return self.repo.create(data)

    def get_list(self) -> QuerySet[models.Application]:
        return self.repo.get_list()

    def get(self, pk: int) -> models.Application:
        return self.repo.get(pk)
