from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path

from chat.consumers import ChatConsumer
from chat.middleware import TokenAuthMiddleware

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        TokenAuthMiddleware(
            URLRouter(
                [
                    path('api/chat/', ChatConsumer.as_asgi()),
                ]
            )
        )
    )
})
