from django.db import models

from users.models import User
from applications.models import ServiceCategory


class PartnerService(models.Model):
    partner = models.ForeignKey(User, on_delete=models.CASCADE)
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.PROTECT)

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=15, decimal_places=2)
