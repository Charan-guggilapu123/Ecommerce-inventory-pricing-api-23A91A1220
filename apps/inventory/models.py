from django.db import models
from apps.products.models.variant import Variant

class Inventory(models.Model):
    variant = models.OneToOneField(Variant, on_delete=models.CASCADE)
    stock_quantity = models.PositiveIntegerField()
    reserved_quantity = models.PositiveIntegerField(default=0)

    @property
    def available_quantity(self):
        return self.stock_quantity - self.reserved_quantity
