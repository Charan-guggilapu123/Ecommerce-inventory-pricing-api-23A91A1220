from django.db import transaction
from .models import Inventory

def reserve_stock(variant_id, qty):
    with transaction.atomic():
        inventory = Inventory.objects.select_for_update().get(variant_id=variant_id)
        if inventory.available_quantity < qty:
            raise ValueError("Insufficient stock")

        inventory.reserved_quantity += qty
        inventory.save()

def release_stock(variant_id, qty):
    with transaction.atomic():
        inventory = Inventory.objects.select_for_update().get(variant_id=variant_id)
        inventory.reserved_quantity -= qty
        inventory.save()
