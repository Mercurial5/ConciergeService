from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import SimpleRouter, NestedSimpleRouter
from chat import views

message_type_router = DefaultRouter()
message_type_router.register('', views.MessageTypeViewSet)

router = SimpleRouter()
router.register('', views.ChatViewSet)

chat_router = NestedSimpleRouter(router, '', lookup='chat')
chat_router.register('messages', views.MessageViewSet, basename='messages')

urlpatterns = [
    path('message-types/', include(message_type_router.urls)),
    path('', include(router.urls)),
    path('', include(chat_router.urls))
]
