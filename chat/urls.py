from rest_framework.routers import DefaultRouter
from chat import views

router = DefaultRouter()
router.register('', views.ChatViewSet)

urlpatterns = router.urls
