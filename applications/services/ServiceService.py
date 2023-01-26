from typing import Protocol, OrderedDict

from django.db.models import QuerySet

from applications import models, repositories


class ServiceServiceInterface(Protocol):
    repo: repositories.ServiceRepositoryInterface

    def create(self, data: OrderedDict) -> models.Service: ...

    def get_list(self, **kwargs) -> QuerySet[models.Service]: ...

    def get(self, pk: int) -> models.Service: ...


class ServiceService:

    def __init__(self):
        self.repo: repositories.ServiceRepositoryInterface = repositories.ServiceRepository()

    def create(self, data: OrderedDict) -> models.Service:
        return self.repo.create(data)

    def get_list(self, **kwargs) -> QuerySet[models.Service]:
        return self.repo.get_list(**kwargs)

    def get(self, pk: int) -> models.Service:
        return self.repo.get(pk)
