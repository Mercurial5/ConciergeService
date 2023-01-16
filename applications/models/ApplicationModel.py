from django.conf import settings
from django.db import models


def get_default_application_status():
    from applications.models import ApplicationStatus

    return ApplicationStatus.get_default_pk()


class Application(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                              related_name='created_applications', null=True)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                related_name='managing_applications', null=True)

    status = models.ForeignKey('applications.ApplicationStatus', on_delete=models.PROTECT,
                               default=get_default_application_status)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    closed = models.DateTimeField(null=True)
