#!/bin/bash

echo ""
echo "======================================"
echo "7-STEP WORKFLOW STATUS CHECK"
echo "======================================"
echo ""

# Database check
echo "Database Status:"
docker exec ecommerce-inventory-pricing-api-23a91a1220-web-1 python manage.py shell -c "
from apps.products.models import Category, Product
from apps.products.models.variant import Variant
from apps.inventory.models import Inventory
from apps.cart.models import Cart, CartItem

print(f'  Categories: {Category.objects.count()}')
print(f'  Products: {Product.objects.count()}')
print(f'  Variants: {Variant.objects.count()}')
print(f'  Inventory: {Inventory.objects.count()}')
print(f'  Carts: {Cart.objects.count()}')
print(f'  Cart Items: {CartItem.objects.count()}')
"

echo ""
echo "Creating Missing Data..."
docker exec ecommerce-inventory-pricing-api-23a91a1220-web-1 python manage.py shell -c "
from apps.products.models import Category, Product
from apps.products.models.variant import Variant
from apps.inventory.models import Inventory

# Step 1-2: Category & Product
cat, _ = Category.objects.get_or_create(name='Clothing')
prod, _ = Product.objects.get_or_create(
    name='T-Shirt',
    defaults={'description': 'Black cotton', 'base_price': 500, 'status': 'active', 'category': cat}
)

# Step 3: Variant
var, _ = Variant.objects.get_or_create(
    sku='TSHIRT-BLK-M',
    defaults={'product': prod, 'attributes': {'size': 'M'}, 'price_adjustment': 50}
)

# Step 4: Inventory
inv, _ = Inventory.objects.get_or_create(variant=var, defaults={'stock_quantity': 10})

print(f'✅ Category ID: {cat.id}')
print(f'✅ Product ID: {prod.id}')
print(f'✅ Variant ID: {var.id}')
print(f'✅ Inventory: Stock={inv.stock_quantity}, Reserved={inv.reserved_quantity}')
"

echo ""
echo "======================================"
echo "STATUS: Steps 1-4 COMPLETED"
echo "======================================"
echo ""
