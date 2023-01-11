from typing import Protocol

from django.db.models import QuerySet

from users import models, repositories


class UserServicesInterface(Protocol):
    repos: repositories.UserRepositoriesInterface

    def get(self, pk: int) -> models.User: ...

    def get_list(self) -> QuerySet[models.User]: ...

    def check_role(self, pk: int, role: str) -> bool: ...


class UserServices:
    repos: repositories.UserRepositoriesInterface = repositories.UserRepositories()

    def get(self, pk: int) -> models.User:
        return self.repos.get(pk)

    def get_list(self) -> QuerySet[models.User]:
        return self.repos.get_list()
