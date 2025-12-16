"""
Test E-commerce Workflow - 7 Steps
"""
from apps.products.models import Category, Product
from apps.products.models.variant import Variant
from apps.inventory.models import Inventory
from apps.cart.models import Cart, CartItem
from apps.pricing.engine import PricingEngine

print("\n" + "="*60)
print("E-COMMERCE WORKFLOW TEST - 7 STEPS")
print("="*60 + "\n")

# Step 1: Create Category
print("Step 1: Create Category")
try:
    category, created = Category.objects.get_or_create(name="Clothing")
    if created:
        print(f"✅ COMPLETED - Category created: {category.name} (ID: {category.id})")
    else:
        print(f"⚠️  EXISTS - Using category: {category.name} (ID: {category.id})")
except Exception as e:
    print(f"❌ FAILED - {e}")
    category = None

# Step 2: Create Product
print("\nStep 2: Create Product")
try:
    if category:
        product, created = Product.objects.get_or_create(
            name="T-Shirt",
            defaults={
                "description": "Black cotton",
                "base_price": 500.00,
                "status": "active",
                "category": category
            }
        )
        if created:
            print(f"✅ COMPLETED - Product created: {product.name} (ID: {product.id})")
        else:
            print(f"⚠️  EXISTS - Using product: {product.name} (ID: {product.id})")
    else:
        product = Product.objects.first()
        print(f"⚠️  Using existing product (ID: {product.id if product else 'None'})")
except Exception as e:
    print(f"❌ FAILED - {e}")
    product = None

# Step 3: Create Variant
print("\nStep 3: Create Variant")
try:
    if product:
        variant, created = Variant.objects.get_or_create(
            sku="TSHIRT-BLK-M",
            defaults={
                "product": product,
                "attributes": {"size": "M"},
                "price_adjustment": 50.00
            }
        )
        if created:
            print(f"✅ COMPLETED - Variant created: {variant.sku} (ID: {variant.id})")
        else:
            print(f"⚠️  EXISTS - Using variant: {variant.sku} (ID: {variant.id})")
    else:
        variant = Variant.objects.first()
        print(f"⚠️  Using existing variant (ID: {variant.id if variant else 'None'})")
except Exception as e:
    print(f"❌ FAILED - {e}")
    variant = None

# Step 4: Add Inventory
print("\nStep 4: Add Inventory")
try:
    if variant:
        inventory, created = Inventory.objects.get_or_create(
            variant=variant,
            defaults={"stock_quantity": 10}
        )
        if created:
            print(f"✅ COMPLETED - Inventory created: Stock={inventory.stock_quantity}")
        else:
            print(f"⚠️  EXISTS - Inventory: Stock={inventory.stock_quantity}, Reserved={inventory.reserved_quantity}")
    else:
        print("⚠️  SKIPPED - No variant available")
except Exception as e:
    print(f"❌ FAILED - {e}")

# Step 5: Test Dynamic Pricing
print("\nStep 5: Test Dynamic Pricing")
try:
    if variant:
        engine = PricingEngine(variant)
        price_data = engine.calculate_price(quantity=10, user_tier="GOLD")
        print(f"✅ COMPLETED - Final Price: {price_data['final_price']}")
        print(f"   Breakdown: {price_data['breakdown']}")
    else:
        print("⚠️  SKIPPED - No variant available")
except Exception as e:
    print(f"❌ FAILED - {e}")

# Step 6: Add to Cart
print("\nStep 6: Add to Cart")
try:
    if variant:
        cart, _ = Cart.objects.get_or_create(user_id=101)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            variant=variant,
            defaults={"quantity": 3, "price": 550.00}
        )
        if created:
            print(f"✅ COMPLETED - Added {cart_item.quantity} items to cart")
        else:
            print(f"⚠️  EXISTS - Cart already has {cart_item.quantity} items")
    else:
        print("⚠️  SKIPPED - No variant available")
except Exception as e:
    print(f"❌ FAILED - {e}")

# Step 7: Verify Reservation
print("\nStep 7: Verify Inventory Reservation")
try:
    if variant:
        inventory = Inventory.objects.get(variant=variant)
        print(f"✅ COMPLETED - Stock: {inventory.stock_quantity}, Reserved: {inventory.reserved_quantity}")
    else:
        print("⚠️  SKIPPED - No variant available")
except Exception as e:
    print(f"❌ FAILED - {e}")

# Summary
print("\n" + "="*60)
print("WORKFLOW TEST SUMMARY")
print("="*60)
print(f"Categories: {Category.objects.count()}")
print(f"Products: {Product.objects.count()}")
print(f"Variants: {Variant.objects.count()}")
print(f"Inventory Records: {Inventory.objects.count()}")
print(f"Carts: {Cart.objects.count()}")
print(f"Cart Items: {CartItem.objects.count()}")
print("="*60 + "\n")
