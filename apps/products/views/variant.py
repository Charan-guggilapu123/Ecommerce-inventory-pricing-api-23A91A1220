from rest_framework.viewsets import ModelViewSet # type: ignore
from apps.products.models.variant import Variant
from apps.products.serializers.variant import VariantSerializer


class VariantViewSet(ModelViewSet):
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer
