import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from chat import models


@database_sync_to_async
def get_chat(pk: int) -> tuple[int, int]:
    try:
        chat = models.Chat.objects.get(pk=pk)
        return chat.manager.id, chat.collocutor.id
    except models.Chat.DoesNotExist:
        return 0, 0


@database_sync_to_async
def create_message(**kwargs):
    models.Message.objects.create(**kwargs)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            str(self.scope['user'].id),
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        self.channel_layer.group_discard(
            str(self.scope['user'].id),
            self.channel_layer
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        chat_id = text_data_json['to']
        message_type_id = text_data_json['message_type_id']

        manager, collocutor = await get_chat(chat_id)

        current_user = self.scope['user']

        if current_user.id in [collocutor, manager]:
            to_user = collocutor if current_user.id == manager else manager

            await create_message(chat_id=chat_id, sender_id=current_user.id, type_id=message_type_id,
                                 content=message)

            await self.channel_layer.group_send(
                str(to_user), {
                    "type": "sendMessage",
                    "message": message,
                    "from": chat_id
                })

    async def sendMessage(self, event):
        await self.send(text_data=json.dumps(event))
