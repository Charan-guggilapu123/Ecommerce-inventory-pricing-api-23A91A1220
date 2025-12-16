from django.db import models
from apps.products.models.variant import Variant

class Cart(models.Model):
    user_id = models.IntegerField()
    status = models.CharField(max_length=20, default="ACTIVE")

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price_snapshot = models.DecimalField(max_digits=10, decimal_places=2)
    reservation_expires_at = models.DateTimeField()
