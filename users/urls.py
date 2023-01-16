from rest_framework.routers import DefaultRouter

from users import views

router = DefaultRouter()
router.register('', views.UserViewSet, basename='users')

urlpatterns = router.urls
