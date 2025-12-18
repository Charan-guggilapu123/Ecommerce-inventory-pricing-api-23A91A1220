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

def checkout(cart):
    with transaction.atomic():
        items = CartItem.objects.select_related("variant").filter(cart=cart)
        
        if not items.exists():
            raise ValueError("Cart is empty")
            
        # 1. Lock and validate inventory for all items
        for item in items:
            # We use select_for_update inside the inventory service or raw here.
            # Ideally we reuse a service method that supports locking, or do it explicitly here 
            # to ensure we lock all relevant rows.
            # Let's use the Inventory model directly to lock.
            from apps.inventory.models import Inventory
            
            inventory = Inventory.objects.select_for_update().get(variant=item.variant)
            
            if inventory.stock_quantity < item.quantity:
                raise ValueError(f"Insufficient stock for {item.variant.sku}")
                
            # 2. Update inventory (Permanent deduction)
            inventory.stock_quantity -= item.quantity
            inventory.reserved_quantity -= item.quantity
            inventory.save()
            
        # 3. Clear cart
        items.delete()
        cart.delete()

