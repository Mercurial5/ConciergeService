from typing import Protocol, OrderedDict

from django.db.models import QuerySet

from partner_services import models, exceptions
from users.models import User


class PartnerServiceRepositoryInterface(Protocol):

    def create(self, data: OrderedDict) -> models.PartnerService: ...

    def list(self) -> QuerySet[models.PartnerService]: ...


class PartnerServiceRepository:
    model = models.PartnerService

    def create(self, data: OrderedDict) -> models.PartnerService:
        partner: User = data['partner']

        if partner.role.name != 'partner':
            raise exceptions.UserIsNotPartner(f'User with id {partner.id} is not a partner.')

        return self.model.objects.create(**data)

    def list(self) -> QuerySet[models.PartnerService]:
        return self.model.objects.all()
