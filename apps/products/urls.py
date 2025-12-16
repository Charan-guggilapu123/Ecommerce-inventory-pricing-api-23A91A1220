from rest_framework.routers import DefaultRouter
from .views.product import ProductViewSet
from .views.category import CategoryViewSet
from .views.variant import VariantViewSet

router = DefaultRouter()
router.register("", ProductViewSet, basename="product")
router.register("categories", CategoryViewSet, basename="category")
router.register("variants", VariantViewSet, basename="variant")

urlpatterns = router.urls
