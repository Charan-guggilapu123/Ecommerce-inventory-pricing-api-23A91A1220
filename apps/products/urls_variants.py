from rest_framework.routers import DefaultRouter
from .views.variant import VariantViewSet

router = DefaultRouter()
router.register("", VariantViewSet, basename="variant")

urlpatterns = router.urls
