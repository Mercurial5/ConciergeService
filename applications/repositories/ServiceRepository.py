from typing import Protocol, OrderedDict

from django.db.models import QuerySet

from applications import models


class ServiceRepositoryInterface(Protocol):
    def create(self, data: OrderedDict) -> models.Service: ...

    def get_list(self, **kwargs) -> QuerySet[models.Service]: ...


class ServiceRepository:
    model = models.Service

    def create(self, data: OrderedDict) -> models.Service:
        return self.model.objects.create(**data)

    def get_list(self, **kwargs) -> QuerySet[models.Service]:
        return self.model.objects.filter(**kwargs).all()
