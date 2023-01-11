from rest_framework.routers import DefaultRouter
from applications import views

router = DefaultRouter()
router.register('', views.ApplicationViewSet, basename='applications')

urlpatterns = router.urls
