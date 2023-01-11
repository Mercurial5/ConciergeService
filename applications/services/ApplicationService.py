from typing import Protocol

from django.db.models import QuerySet

from applications import models
from applications.repositories import ApplicationRepositoryInterface, ApplicationRepository
from users.services import UserServiceInterface


class ApplicationServiceInterface(Protocol):
    repos: ApplicationRepositoryInterface

    def create(self, owner_id: int, manager_id: int) -> models.Application: ...

    def get_list(self) -> QuerySet[models.Application]: ...


class ApplicationService:

    def __init__(self, user_repos: UserServiceInterface):
        self.repos: ApplicationRepositoryInterface = ApplicationRepository(user_repos)

    def create(self, owner_id: int, manager_id: int) -> models.Application:
        return self.repos.create(owner_id, manager_id)

    def get_list(self) -> QuerySet[models.Application]:
        return self.repos.get_list()
