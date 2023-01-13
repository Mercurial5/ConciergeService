from django.db import models
from applications import models as my_models


class Service(models.Model):
    service_category = models.ForeignKey(my_models.ServiceCategory, on_delete=models.PROTECT)
    application = models.ForeignKey(my_models.Application, on_delete=models.PROTECT)

    description = models.TextField()
    date_from = models.DateTimeField(null=True)
    date_to = models.DateTimeField(null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
