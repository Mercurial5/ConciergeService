from typing import Protocol, OrderedDict

from django.db.models import QuerySet

from applications import models


class ServiceRepositoryInterface(Protocol):
    def create(self, data: OrderedDict) -> models.Service: ...

    def get_list(self) -> QuerySet[models.Service]: ...


class ServiceRepository:
    model = models.Service

    def create(self, data: OrderedDict) -> models.Service:
        print(data)
        return self.model.objects.create(**data)

    def get_list(self) -> QuerySet[models.Service]:
        return self.model.objects.all()
