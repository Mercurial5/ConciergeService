from rest_framework import serializers
from chat import models


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chat
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        last_message = models.Message.objects.filter(chat_id=data['id']).order_by('id').last()
        data['last_message'] = MessageSerializer(last_message).data
        return data


class MessageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Chat
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = '__all__'
