from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users import views

users_router = DefaultRouter()
users_router.register('', views.UserViewSet, basename='users')

roles_router = DefaultRouter()
roles_router.register('', views.RolesViewSet, basename='roles')

city_router = DefaultRouter()
city_router.register('', views.CitiesViewSet, basename='cities')

urlpatterns = [
    path('roles/', include(roles_router.urls)),
    path('cities/', include(city_router.urls)),
    path('', include(users_router.urls))
]
