from django.db import models
from users.models import User
from applications.models import Application


class Chat(models.Model):
    application = models.ForeignKey(Application, on_delete=models.PROTECT)
    manager = models.ForeignKey(User, on_delete=models.PROTECT, related_name='chats_manager')
    collocutor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='chats')

    class Meta:
        unique_together = ('application', 'manager', 'collocutor')


class MessageType(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.PROTECT)
    sender = models.ForeignKey(User, on_delete=models.PROTECT)
    type = models.ForeignKey(MessageType, on_delete=models.PROTECT)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
