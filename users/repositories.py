from typing import Protocol

from django.db.models import QuerySet

from users import models, exceptions


class UserRepositoriesInterface(Protocol):

    def get(self, pk: int) -> models.User: ...

    def get_list(self) -> QuerySet[models.User]: ...

    def check_role(self, pk: int, role: str) -> bool: ...


class UserRepositories:
    model = models.User

    def get(self, pk: int) -> models.User:
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise exceptions.UserDoesNotExist(f'User with id {pk} does not exist.')

    def get_list(self) -> QuerySet[models.User]:
        return self.model.objects.all()

    def check_role(self, pk: int, role: str) -> bool:
        try:
            role = models.Role.objects.filter(name=role)
        except models.Role.DoesNotExist:
            raise exceptions.RoleDoesNotExist(f'Role with name {role} does not exist.')

        user = self.get(pk)
        return user.role.name == role
