from typing import Protocol, OrderedDict

from django.db.models import QuerySet

from partner_services import models, repositories


class PartnerServiceServiceInterface(Protocol):
    repo: repositories.PartnerServiceRepositoryInterface

    def create(self, data: OrderedDict) -> models.PartnerService: ...

    def list(self) -> QuerySet[models.PartnerService]: ...


class PartnerServiceService:
    repo: repositories.PartnerServiceRepositoryInterface = repositories.PartnerServiceRepository()

    def create(self, data: OrderedDict) -> models.PartnerService:
        return self.repo.create(data)

    def list(self) -> QuerySet[models.PartnerService]:
        return self.repo.list()
