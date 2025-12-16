from rest_framework import serializers # type: ignore
from apps.products.models.product import Product # type: ignore

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
