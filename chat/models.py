from django.db import models
from users.models import User


class Chat(models.Model):
    manager = models.ForeignKey(User, on_delete=models.PROTECT, related_name='chats_manager')
    collocutor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='chats')
