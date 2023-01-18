from typing import Protocol, OrderedDict

from django.db.models import QuerySet

from users import models, exceptions


class UserRepositoryInterface(Protocol):

    def get(self, pk: int) -> models.User: ...

    def get_list(self) -> QuerySet[models.User]: ...

    def create(self, data: OrderedDict) -> models.User: ...

    def set_password(self, user: models.User, password: str = None) -> str: ...

    @staticmethod
    def activate(user: models.User): ...

    def delete(self, pk: int): ...


class UserRepository:
    model = models.User

    def get(self, pk: int) -> models.User:
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise exceptions.UserDoesNotExist(f'User with id {pk} does not exist.')

    def get_list(self) -> QuerySet[models.User]:
        return self.model.objects.all()

    def create(self, data: OrderedDict) -> models.User:
        user = self.model.objects.create(**data)

        return user

    def set_password(self, user: models.User, password: str = None) -> str:
        if password is None:
            password = self.model.objects.make_random_password()

        user.set_password(password)
        user.save(update_fields=['password'])

        return password

    @staticmethod
    def activate(user: models.User):
        user.is_active = True
        user.save(update_fields=['is_active'])

    def delete(self, pk: int):
        self.model.objects.get(pk=pk).delete()
