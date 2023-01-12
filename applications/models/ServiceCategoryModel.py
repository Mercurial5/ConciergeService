from django.db import models


class ServiceCategory(models.Model):
    parent_id = models.ForeignKey('self', on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=255)
