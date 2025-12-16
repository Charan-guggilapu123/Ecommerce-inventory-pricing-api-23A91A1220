from django.db import models
from .product import Product

class Variant(models.Model):
    product = models.ForeignKey(Product, related_name="variants", on_delete=models.CASCADE)
    sku = models.CharField(max_length=100, unique=True)
    attributes = models.JSONField()
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.sku
