from django.conf import settings
from django.db import models

from applications import models as my_models


class Application(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                              related_name='created_applications', null=True)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                related_name='managing_applications', null=True)

    status = models.OneToOneField(my_models.ApplicationStatus, on_delete=models.PROTECT, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    closed = models.DateTimeField(null=True)
