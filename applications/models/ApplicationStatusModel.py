from django.db import models


class ApplicationStatus(models.Model):
    name = models.CharField(max_length=255)
