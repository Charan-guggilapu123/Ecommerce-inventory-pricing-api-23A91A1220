from rest_framework import serializers
from apps.products.models.variant import Variant


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ['id', 'product', 'sku', 'attributes', 'price_adjustment']
