from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import SimpleRouter, NestedSimpleRouter

from applications import views

router = SimpleRouter()
router.register('', views.ApplicationViewSet, basename='applications')

applications_router = NestedSimpleRouter(router, '', lookup='application')
applications_router.register('services', views.ServiceViewSet, basename='services')

service_category_router = DefaultRouter()
service_category_router.register('', views.ServiceCategoryView)

urlpatterns = [
    path('create-first-application/', views.create_first_application),
    path('categories/', include(service_category_router.urls)),

    path('', include(router.urls)),
    path('', include(applications_router.urls)),
]
