from typing import Protocol

from django.db.models import QuerySet

from users import models, repositories


class UserServiceInterface(Protocol):
    repos: repositories.UserRepositoryInterface

    def get(self, pk: int) -> models.User: ...

    def get_list(self) -> QuerySet[models.User]: ...

    def check_role(self, pk: int, role: str) -> bool: ...


class UserService:
    repos: repositories.UserRepositoryInterface = repositories.UserRepository()

    def get(self, pk: int) -> models.User:
        return self.repos.get(pk)

    def get_list(self) -> QuerySet[models.User]:
        return self.repos.get_list()
