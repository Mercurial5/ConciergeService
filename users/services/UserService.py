from typing import Protocol, OrderedDict

from django.db.models import QuerySet

from users import models, repositories


class UserServiceInterface(Protocol):
    repo: repositories.UserRepositoryInterface

    def get(self, pk: int) -> models.User: ...

    def get_list(self) -> QuerySet[models.User]: ...

    def create(self, data: OrderedDict) -> models.User: ...

    def set_password(self, user: models.User, password: str = None) -> str: ...

    def activate(self, user: models.User): ...

    def delete(self, pk: int): ...


class UserService:
    repo: repositories.UserRepositoryInterface = repositories.UserRepository()

    def get(self, pk: int) -> models.User:
        return self.repo.get(pk)

    def get_list(self) -> QuerySet[models.User]:
        return self.repo.get_list()

    def create(self, data: OrderedDict) -> models.User:
        return self.repo.create(data)

    def set_password(self, user: models.User, password: str = None) -> str:
        return self.repo.set_password(user, password)

    def activate(self, user: models.User):
        self.repo.activate(user)

    def delete(self, pk: int):
        self.repo.delete(pk)