from rest_framework.viewsets import ModelViewSet # type: ignore
from apps.products.models.product import Product # type: ignore
from apps.products.serializers.product import ProductSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
