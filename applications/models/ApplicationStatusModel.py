from django.db import models


class ApplicationStatus(models.Model):
    name = models.CharField(max_length=255, unique=True)

    @staticmethod
    def get_default_pk():
        status, created = ApplicationStatus.objects.get_or_create(name='Not Started')
        return status.pk
