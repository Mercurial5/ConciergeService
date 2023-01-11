from typing import Protocol

from django.db.models import QuerySet

from users import models, exceptions


class UserRepositoryInterface(Protocol):

    def get(self, pk: int) -> models.User: ...

    def get_list(self) -> QuerySet[models.User]: ...

    def check_role(self, pk: int, role: str) -> bool: ...


class UserRepository:
    model = models.User

    def get(self, pk: int) -> models.User:
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise exceptions.UserDoesNotExist(f'User with id {pk} does not exist.')

    def get_list(self) -> QuerySet[models.User]:
        return self.model.objects.all()
