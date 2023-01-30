from rest_framework import serializers
from chat import models
from users.serializers import UserOuterSerializer
from users.models import User


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chat
        fields = '__all__'


class ChatReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chat
        exclude = ['manager']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        last_message = models.Message.objects.filter(chat_id=data['id']).order_by('id').last()
        data['last_message'] = MessageSerializer(last_message).data

        collocutor = User.objects.get(pk=data['collocutor'])
        data['collocutor'] = UserOuterSerializer(collocutor).data
        return data


class MessageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chat
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = '__all__'
