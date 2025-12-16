import threading
import pytest # type: ignore
from django.db import transaction
from apps.inventory.models import Inventory
from apps.inventory.services import reserve_stock
from apps.products.models.product import Product
from apps.products.models.variant import Variant
from apps.products.models.category import Category

pytestmark = pytest.mark.django_db(transaction=True)

def setup_inventory(stock=10):
    category = Category.objects.create(name="Clothing")
    product = Product.objects.create(
        name="T-Shirt",
        description="Black",
        base_price=500,
        status="active",
        category=category
    )
    variant = Variant.objects.create(
        product=product,
        sku="TSHIRT-BLK-M",
        attributes={"size": "M"}
    )
    inventory = Inventory.objects.create(
        variant=variant,
        stock_quantity=stock
    )
    return inventory

def try_reserve(inventory, qty, results, index):
    try:
        reserve_stock(inventory.variant.id, qty)
        results[index] = "SUCCESS"
    except Exception:
        results[index] = "FAIL"

def test_concurrent_reservations_no_oversell():
    inventory = setup_inventory(stock=10)

    results = {}
    threads = []

    # 5 threads trying to reserve 3 each (total 15 > 10)
    for i in range(5):
        t = threading.Thread(
            target=try_reserve,
            args=(inventory, 3, results, i)
        )
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    inventory.refresh_from_db()

    assert inventory.reserved_quantity <= 10
    assert list(results.values()).count("SUCCESS") == 3
    assert list(results.values()).count("FAIL") == 2
