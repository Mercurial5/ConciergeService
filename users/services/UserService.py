from typing import Protocol

from django.db.models import QuerySet

from users import models, repositories


class UserServiceInterface(Protocol):
    repo: repositories.UserRepositoryInterface

    def get(self, pk: int) -> models.User: ...

    def get_list(self) -> QuerySet[models.User]: ...


class UserService:
    repo: repositories.UserRepositoryInterface = repositories.UserRepository()

    def get(self, pk: int) -> models.User:
        return self.repo.get(pk)

    def get_list(self) -> QuerySet[models.User]:
        return self.repo.get_list()
