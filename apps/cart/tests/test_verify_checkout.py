
import pytest
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
from apps.products.models.category import Category
from apps.products.models.product import Product
from apps.products.models.variant import Variant
from apps.inventory.models import Inventory
from apps.cart.models import Cart, CartItem
from apps.cart.services import add_to_cart, checkout
from apps.pricing.models import PricingRule
from apps.pricing.engine import PricingEngine

pytestmark = pytest.mark.django_db

def test_seasonal_pricing():
    print("\n=== Testing Seasonal Pricing ===")
    
    # Setup Rule
    rule = PricingRule.objects.create(
        rule_type="SEASONAL",
        priority=1,
        config={
            "start_date": (timezone.now() - timedelta(days=1)).isoformat(),
            "end_date": (timezone.now() + timedelta(days=1)).isoformat(),
            "discount_percent": 20
        },
        is_active=True
    )
    
    engine = PricingEngine()
    base_price = Decimal("100.00")
    
    # Calculate
    final_price, breakdown = engine.calculate(base_price, 1)
    
    # cleanup
    rule.delete()

    assert final_price == Decimal("80.00")
    

def test_checkout_flow():
    print("\n=== Testing Checkout Flow ===")
    
    # 1. Setup Data
    cat = Category.objects.create(name="TestCat")
    prod = Product.objects.create(name="TestProd", base_price=100, status="active", category=cat)
    var = Variant.objects.create(product=prod, sku="SKU123", attributes={}, price_adjustment=0)
    inv = Inventory.objects.create(variant=var, stock_quantity=10, reserved_quantity=0)
    
    # 2. Add to Cart
    user_id = 999
    cart, _ = Cart.objects.get_or_create(user_id=user_id)
    add_to_cart(cart, var, 2, Decimal("100.00"))
    
    inv.refresh_from_db()
    assert inv.reserved_quantity == 2
    
    # 3. Checkout
    checkout(cart)
    
    inv.refresh_from_db()
    
    assert inv.stock_quantity == 8
    assert inv.reserved_quantity == 0
    assert not Cart.objects.filter(id=cart.id).exists()
    
