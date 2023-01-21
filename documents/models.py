from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    document = models.FileField(upload_to='documents/docs/')
