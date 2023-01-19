from rest_framework.routers import DefaultRouter

from partner_services import views

router = DefaultRouter()
router.register('', views.PartnerServicesViewSet, basename='partner-services')

urlpatterns = router.urls
