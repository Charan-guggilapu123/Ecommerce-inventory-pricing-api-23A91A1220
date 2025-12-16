from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from apps.inventory.services import reserve_stock
from .models import CartItem

def add_to_cart(cart, variant, quantity, price):
    reserve_stock(variant.id, quantity)

    CartItem.objects.create(
        cart=cart,
        variant=variant,
        quantity=quantity,
        price_snapshot=price,
        reservation_expires_at=timezone.now() + timedelta(minutes=15)
    )
