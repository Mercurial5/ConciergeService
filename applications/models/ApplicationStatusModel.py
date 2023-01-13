from django.db import models


class ApplicationStatus(models.Model):
    name = models.CharField(max_length=255)

    @staticmethod
    def get_default_pk():
        status, created = ApplicationStatus.objects.get_or_create(name='Pending')
        return status.pk
