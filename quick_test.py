from apps.products.models import Category, Product
from apps.products.models.variant import Variant
from apps.inventory.models import Inventory

print('\n' + '='*60)
print('TESTING 7-STEP WORKFLOW')
print('='*60)

# Current state
print(f'\nCurrent State:')
print(f'  Categories: {Category.objects.count()}')
print(f'  Products: {Product.objects.count()}')
print(f'  Variants: {Variant.objects.count()}')
print(f'  Inventory: {Inventory.objects.count()}')

# Step 1-4: Create test data
print(f'\nCreating test data...')
cat, _ = Category.objects.get_or_create(name='Clothing')
print(f'✅ Category: {cat.id} - {cat.name}')

prod, _ = Product.objects.get_or_create(
    name='T-Shirt',
    defaults={'description': 'Black cotton', 'base_price': 500, 'status': 'active', 'category': cat}
)
print(f'✅ Product: {prod.id} - {prod.name}')

var, _ = Variant.objects.get_or_create(
    sku='TSHIRT-BLK-M',
    defaults={'product': prod, 'attributes': {'size': 'M'}, 'price_adjustment': 50}
)
print(f'✅ Variant: {var.id} - {var.sku}')

inv, _ = Inventory.objects.get_or_create(variant=var, defaults={'stock_quantity': 10})
print(f'✅ Inventory: Stock={inv.stock_quantity}, Reserved={inv.reserved_quantity}')

print('\n' + '='*60)
print('STEPS 1-4 COMPLETED')
print('='*60 + '\n')
