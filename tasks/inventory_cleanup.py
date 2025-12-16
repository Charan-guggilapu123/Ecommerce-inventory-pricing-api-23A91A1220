from celery import shared_task # type: ignore
from django.utils import timezone
from django.db import transaction
from apps.cart.models import CartItem
from apps.inventory.models import Inventory

@shared_task
def release_expired_reservations():
    expired = CartItem.objects.filter(reservation_expires_at__lt=timezone.now())

    for item in expired:
        with transaction.atomic():
            inventory = Inventory.objects.select_for_update().get(
                variant=item.variant
            )
            inventory.reserved_quantity -= item.quantity
            inventory.save()
            item.delete()
