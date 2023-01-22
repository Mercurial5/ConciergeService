from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class DocumentType(models.Model):
    name = models.CharField(max_length=255)


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(DocumentType, on_delete=models.PROTECT)

    name = models.CharField(max_length=255)
    document = models.FileField(upload_to='media/docs/')
