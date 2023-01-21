from rest_framework.routers import DefaultRouter

from documents import views

router = DefaultRouter()
router.register('', views.DocumentViewSet)

urlpatterns = router.urls
