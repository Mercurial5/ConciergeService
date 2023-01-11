from typing import Protocol

from django.db.models import QuerySet

from applications import models
from applications.repositories import ApplicationRepositoryInterface, ApplicationRepository
from users.services import UserServiceInterface


class ApplicationServiceInterface(Protocol):
    repo: ApplicationRepositoryInterface

    def create(self, **kwargs) -> models.Application: ...

    def get_list(self) -> QuerySet[models.Application]: ...


class ApplicationService:

    def __init__(self, user_repo: UserServiceInterface):
        self.repo: ApplicationRepositoryInterface = ApplicationRepository(user_repo)

    def create(self, **kwargs) -> models.Application:
        return self.repo.create(**kwargs)

    def get_list(self) -> QuerySet[models.Application]:
        return self.repo.get_list()
