from rest_framework.routers import DefaultRouter
from django.urls import path, include

from documents import views

documents_router = DefaultRouter()
documents_router.register('', views.DocumentViewSet)

document_types_router = DefaultRouter()
document_types_router.register('', views.DocumentTypeViewSet)

urlpatterns = [
    path('types/', include(document_types_router.urls)),
    path('', include(documents_router.urls))
]
