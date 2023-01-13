from django.urls import path, include
from rest_framework_nested.routers import SimpleRouter, NestedSimpleRouter
from applications import views

router = SimpleRouter()
router.register('', views.ApplicationViewSet, basename='applications')

applications_router = NestedSimpleRouter(router, '', lookup='application')
applications_router.register('services', views.ServiceViewSet, basename='services')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(applications_router.urls))
]
