# Database Schema & Entity Relationship Diagram

## Complete ERD (Entity Relationship Diagram)

```
┌─────────────────────────────┐
│      CATEGORIES             │
├─────────────────────────────┤
│ PK │ id (BigAutoField)      │
│    │ name (CharField)       │
│    │ description (Text)     │
│    │ parent_id (ForeignKey) │◄─────────┐
│    │ created_at (DateTime)  │          │
│    │ updated_at (DateTime)  │          │
│ IX │ name (indexed)         │          │
│ IX │ parent_id (indexed)    │          │
└─────────────────────────────┘          │
         │                               │
         │ 1:N (parent_id)              │
         └───────────────────────────────┘
         │
         │ 1:N (category_id)
         │
         ▼
┌─────────────────────────────────┐
│      PRODUCTS                   │
├─────────────────────────────────┤
│ PK │ id (BigAutoField)          │
│ FK │ category_id (ForeignKey)   │──────────┐
│    │ name (CharField)           │          │
│    │ description (Text)         │          │
│    │ base_price (DecimalField)  │          │
│    │ created_at (DateTime)      │          │
│    │ updated_at (DateTime)      │          │
│ IX │ name (indexed)             │          │
│ IX │ category_id (indexed)      │          │
└─────────────────────────────────┘          │
         │                                   │
         │ 1:N (product_id)                 │
         │                                   │
         ▼                                   │
┌──────────────────────────────┐             │
│      VARIANTS                │             │
├──────────────────────────────┤             │
│ PK │ id (BigAutoField)       │             │
│ FK │ product_id (ForeignKey) │─────────────┘
│    │ sku (CharField, unique) │
│    │ attributes (JSONField)  │
│    │ price_adjustment        │
│    │ (DecimalField)          │
│    │ is_active (Boolean)     │
│    │ created_at (DateTime)   │
│    │ updated_at (DateTime)   │
│ IX │ sku (unique indexed)    │
│ IX │ product_id (indexed)    │
└──────────────────────────────┘
         │
         │ 1:N (variant_id)
         │
         ▼
┌────────────────────────────────────┐
│      INVENTORY                     │
├────────────────────────────────────┤
│ PK │ id (BigAutoField)             │
│ FK │ variant_id (ForeignKey)       │
│    │ quantity (IntegerField)       │
│    │ reserved_quantity (IntField)  │
│    │ available_quantity             │
│    │ (Computed: qty - reserved)    │
│    │ last_stock_check (DateTime)   │
│    │ updated_at (DateTime)         │
│ IX │ variant_id (unique indexed)   │
│ UQ │ variant_id (unique)           │
│ CK │ quantity >= 0                 │
│ CK │ reserved_qty >= 0             │
│ CK │ reserved_qty <= quantity      │
└────────────────────────────────────┘
         │
         │
         └─────────────────────┐
                               │
         ┌─────────────────────┴──────────────────┐
         │                                        │
         │ SELECT FOR UPDATE                      │
         │ (Pessimistic Lock)                     │
         │                                        │
         ▼                                        │
┌──────────────────────────┐                     │
│      RESERVATIONS        │                     │
├──────────────────────────┤                     │
│ PK │ id (BigAutoField)   │                     │
│ FK │ user_id (IntField)  │                     │
│    │ status (CharField)  │◄─ ACTIVE           │
│    │ expires_at (DT)     │◄─ 5 min from now  │
│    │ created_at (DT)     │                     │
│ IX │ status (indexed)    │                     │
│ IX │ expires_at (indexed)│ ◄─ For cleanup     │
│ IX │ user_id (indexed)   │                     │
└──────────────────────────┘                     │
         ▲                                       │
         │ 1:N                                   │
         │ (reservation_id)                      │
         │                                       │
         │                    ┌──────────────────┘
         │                    │
         │                    │ 1:N (variant_id)
         │                    │
         │                    ▼
         │            ┌──────────────────────────┐
         │            │    CART_ITEMS            │
         │            ├──────────────────────────┤
         │            │ PK │ id (BigAutoField)   │
         │            │ FK │ cart_id (Foreign)  │──┐
         │            │ FK │ product_id (F-Key) │  │
         │            │    │ quantity (IntField)│  │
         │            │    │ price_snapshot     │  │
         │            │    │ (DecimalField)     │  │
         │            │    │ created_at (DT)    │  │
         │            │ IX │ cart_id (indexed)  │  │
         │            │ IX │ product_id (indx)  │  │
         │            └──────────────────────────┘  │
         │                    ▲                     │
         │                    │ 1:N                 │
         │                    │ (cart_id)           │
         │                    │                     │
         │            ┌───────┴──────────────┐     │
         │            │                      │     │
         │            ▼                      │     │
         │    ┌──────────────┐               │     │
         │    │    CART      │               │     │
         │    ├──────────────┤               │     │
         │    │ PK │ id (BA) │               │     │
         │    │ FK │ user_id │               │     │
         │    │    │ created │               │     │
         │    │    │ updated │               │     │
         │    │ IX │ user_id │               │     │
         │    └──────────────┘               │     │
         │            │                      │     │
         └────────────┼──────────────────────┘     │
                      │ (cart.id = cart_items.cart_id)
                      │
                      └───────────────────────┘
                        (payment info stored
                         in Reservation)

     PRICING_RULES (Optional Separate Table)
     ┌──────────────────────────────┐
     │ PK │ id                       │
     │    │ rule_type (quantity,etc.)│
     │    │ condition_value          │
     │    │ discount_percent         │
     │    │ priority (for ordering)  │
     │    │ is_active                │
     └──────────────────────────────┘
```

## Detailed Table Schemas

### 1. CATEGORIES Table
```sql
CREATE TABLE products_category (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    parent_id BIGINT REFERENCES products_category(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE AUTO_NOW_ADD,
    updated_at TIMESTAMP WITH TIME ZONE AUTO_NOW,
    
    UNIQUE (name, parent_id),  -- Prevent duplicate subcategories
    INDEX idx_name (name),
    INDEX idx_parent_id (parent_id)
);

Sample Data:
┌────┬───────────┬─────────────────┬───────────┐
│ id │ name      │ description     │ parent_id │
├────┼───────────┼─────────────────┼───────────┤
│ 1  │ Clothing  │ Apparel items   │ NULL      │
│ 2  │ Men       │ Men's clothing  │ 1         │
│ 3  │ Women     │ Women's clothing│ 1         │
│ 4  │ Shirts    │ Shirt variants  │ 2         │
└────┴───────────┴─────────────────┴───────────┘
```

### 2. PRODUCTS Table
```sql
CREATE TABLE products_product (
    id BIGSERIAL PRIMARY KEY,
    category_id BIGINT NOT NULL REFERENCES products_category(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    base_price DECIMAL(10,2) NOT NULL CHECK (base_price > 0),
    created_at TIMESTAMP WITH TIME ZONE AUTO_NOW_ADD,
    updated_at TIMESTAMP WITH TIME ZONE AUTO_NOW,
    
    INDEX idx_name (name),
    INDEX idx_category_id (category_id)
);

Sample Data:
┌────┬───────┬──────────┬────────────────┐
│ id │ name  │ base_pri │ category_id    │
├────┼───────┼──────────┼────────────────┤
│ 1  │ T-Shrt│  500.00  │ 4 (Shirts)     │
│ 2  │ Jeans │  800.00  │ 4              │
└────┴───────┴──────────┴────────────────┘
```

### 3. VARIANTS Table
```sql
CREATE TABLE products_variant (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT NOT NULL REFERENCES products_product(id),
    sku VARCHAR(255) NOT NULL UNIQUE,
    attributes JSONB,  -- {"color": "black", "size": "M"}
    price_adjustment DECIMAL(10,2) DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE AUTO_NOW_ADD,
    updated_at TIMESTAMP WITH TIME ZONE AUTO_NOW,
    
    UNIQUE (sku),
    INDEX idx_sku (sku),
    INDEX idx_product_id (product_id)
);

Sample Data:
┌────┬────────┬──────────────┬──────────────┬──────────┐
│ id │ product│ sku          │ attributes   │ adj_price│
├────┼────────┼──────────────┼──────────────┼──────────┤
│ 1  │ 1      │ TSHIRT-BLK-M │ {"c":"black",│  50.00   │
│    │        │              │ "s":"M"}     │          │
│ 2  │ 1      │ TSHIRT-RED-L │ {"c":"red",  │  50.00   │
│    │        │              │ "s":"L"}     │          │
└────┴────────┴──────────────┴──────────────┴──────────┘
```

### 4. INVENTORY Table
```sql
CREATE TABLE inventory_inventory (
    id BIGSERIAL PRIMARY KEY,
    variant_id BIGINT NOT NULL UNIQUE REFERENCES products_variant(id),
    quantity INTEGER NOT NULL CHECK (quantity >= 0),
    reserved_quantity INTEGER NOT NULL DEFAULT 0 CHECK (reserved_quantity >= 0),
    last_stock_check TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE AUTO_NOW,
    
    CHECK (reserved_quantity <= quantity),
    UNIQUE (variant_id),
    INDEX idx_variant_id (variant_id)
);

Sample Data:
┌────┬───────┬──────┬────────┬───────────────────┐
│ id │ var_id│ qty  │ reserved│ available (computed)
├────┼───────┼──────┼────────┼──────────────────┤
│ 1  │ 1     │ 10   │ 3      │ 7                 │
│ 2  │ 2     │ 15   │ 5      │ 10                │
└────┴───────┴──────┴────────┴──────────────────┘

** CRITICAL: Locked with SELECT FOR UPDATE during checkout **
```

### 5. CART Table
```sql
CREATE TABLE cart_cart (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,  -- Can extend with user auth
    created_at TIMESTAMP WITH TIME ZONE AUTO_NOW_ADD,
    updated_at TIMESTAMP WITH TIME ZONE AUTO_NOW,
    
    INDEX idx_user_id (user_id)
);

Sample Data:
┌────┬─────────┬────────────┐
│ id │ user_id │ created_at │
├────┼─────────┼────────────┤
│ 1  │ 123     │ 2025-12-17│
│ 2  │ 456     │ 2025-12-17│
└────┴─────────┴────────────┘
```

### 6. CART_ITEMS Table
```sql
CREATE TABLE cart_cartitem (
    id BIGSERIAL PRIMARY KEY,
    cart_id BIGINT NOT NULL REFERENCES cart_cart(id) ON DELETE CASCADE,
    product_id BIGINT NOT NULL REFERENCES products_product(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price_snapshot DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE AUTO_NOW_ADD,
    
    INDEX idx_cart_id (cart_id),
    INDEX idx_product_id (product_id)
);

Sample Data:
┌────┬────────┬──────────┬──────┬───────────┐
│ id │ cart_id│ prod_id  │ qty  │ price_snap│
├────┼────────┼──────────┼──────┼───────────┤
│ 1  │ 1      │ 1        │ 2    │ 420.75    │
│ 2  │ 1      │ 2        │ 1    │ 750.00    │
└────┴────────┴──────────┴──────┴───────────┘
```

### 7. RESERVATIONS Table
```sql
CREATE TABLE cart_reservation (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',  -- ACTIVE, EXPIRED, COMPLETED
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE AUTO_NOW_ADD,
    
    CHECK (status IN ('ACTIVE', 'EXPIRED', 'COMPLETED')),
    INDEX idx_status (status),
    INDEX idx_expires_at (expires_at),  -- For cleanup query
    INDEX idx_user_id (user_id)
);

Sample Data:
┌────┬─────────┬────────┬─────────────────┐
│ id │ user_id │ status │ expires_at      │
├────┼─────────┼────────┼─────────────────┤
│ 1  │ 123     │ ACTIVE │ 2025-12-17 12:05│  (5 min from now)
│ 2  │ 456     │ EXPIRED│ 2025-12-17 11:50│  (cleanup ready)
└────┴─────────┴────────┴─────────────────┘
```

## Indexes Strategy

### Primary Key Indexes (Automatic)
- `categories.id`, `products.id`, `variants.id`, etc.

### Foreign Key Indexes (Best Practices)
- `products.category_id` - For joins in category listing
- `variants.product_id` - For product detail/variants
- `inventory.variant_id` - For availability checks
- `cartitem.cart_id` - For cart contents
- `cartitem.product_id` - For product lookup

### Search/Filter Indexes
- `categories.name` - For category search
- `products.name` - For product search
- `variants.sku` - For SKU lookup (unique index)

### Query Performance Indexes
- `reservations.expires_at` - **CRITICAL** for cleanup job
- `reservations.status` - For filtering active reservations
- `cart.user_id` - For user's cart retrieval

### Unique Constraints
- `variants.sku` - Prevent duplicate SKUs
- `inventory.variant_id` - One inventory per variant
- `categories.name` + `parent_id` - Prevent duplicate subcategories

## Transaction Flow & Locking

### Checkout Transaction (SERIALIZABLE isolation)
```
BEGIN TRANSACTION;
  ├─ SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
  │
  ├─ FOR each CartItem:
  │  │
  │  ├─ SELECT * FROM inventory 
  │  │  WHERE variant_id = ? 
  │  │  FOR UPDATE;          ◄─── PESSIMISTIC LOCK
  │  │
  │  ├─ IF quantity < cart_qty:
  │  │  │  ROLLBACK;
  │  │  │  RAISE "Insufficient stock"
  │  │  └─ (other user waiting here releases)
  │  │
  │  └─ UPDATE inventory 
  │     SET reserved_quantity = reserved_quantity + cart_qty
  │     WHERE variant_id = ?
  │
  ├─ INSERT INTO cart_reservation (...)
  │
  ├─ DELETE FROM cart_cartitem WHERE cart_id = ?
  │
  ├─ DELETE FROM cart_cart WHERE id = ?
  │
  └─ COMMIT;
     (Lock released, next waiting user acquires lock)
```

### Cleanup Transaction (Async via Celery)
```
SELECT * FROM cart_reservation
WHERE status = 'ACTIVE' 
  AND expires_at < NOW()
INDEX: expires_at
```

## Data Integrity Constraints

### Check Constraints
```
Inventory:
  ✓ quantity >= 0
  ✓ reserved_quantity >= 0
  ✓ reserved_quantity <= quantity

Products:
  ✓ base_price > 0

Variants:
  ✓ price_adjustment >= 0 (or can be negative)

CartItems:
  ✓ quantity > 0

Reservations:
  ✓ status IN ('ACTIVE', 'EXPIRED', 'COMPLETED')
```

### Referential Integrity
```
Categories ← Products (parent_id nullable for root)
Products ← Variants
Variants ← Inventory (1:1 unique)
Cart ← CartItems (ON DELETE CASCADE)
Reservation ← (via user_id foreign key to users table)
```

## Query Performance Analysis

### High-Frequency Queries

#### 1. List Products by Category
```sql
SELECT p.*, c.name as category_name
FROM products_product p
JOIN products_category c ON p.category_id = c.id
WHERE p.category_id = ?
ORDER BY p.created_at DESC;

Cost: O(log N) - uses category_id index
```

#### 2. Get Product with Variants & Inventory
```sql
SELECT p.*, v.*, i.quantity, i.reserved_quantity
FROM products_product p
LEFT JOIN products_variant v ON p.id = v.product_id
LEFT JOIN inventory_inventory i ON v.id = i.variant_id
WHERE p.id = ?;

Cost: O(log N) - uses product_id index
```

#### 3. Get Cart Contents
```sql
SELECT ci.*, p.name, p.base_price
FROM cart_cartitem ci
JOIN products_product p ON ci.product_id = p.id
WHERE ci.cart_id = ?;

Cost: O(M) where M = cart items (typically 5-20)
```

#### 4. Cleanup Expired Reservations (Celery)
```sql
SELECT * FROM cart_reservation
WHERE status = 'ACTIVE' 
  AND expires_at < NOW();

Cost: O(log N) - uses expires_at index
Frequency: Every 5 minutes
```

#### 5. Checkout (Most Complex)
```sql
FOR each variant in cart:
  SELECT * FROM inventory 
  WHERE variant_id = ? 
  FOR UPDATE;  -- Lock + fetch
  
UPDATE inventory SET reserved_quantity = ?
WHERE variant_id = ?;  -- Update

INSERT INTO cart_reservation (...);
DELETE FROM cart_cartitem WHERE cart_id = ?;
DELETE FROM cart_cart WHERE id = ?;

Cost: O(M log N) where M = items in cart
Locking: 50-100ms per variant (depends on contention)
```

## Backup & Recovery Strategy

### Backup Frequency
- **Full Backup**: Daily (off-peak hours)
- **Transaction Log**: Continuous (WAL in PostgreSQL)
- **Point-in-Time Recovery**: 7 days retention

### Disaster Recovery
```
Scenario: Corruption or data loss
├─ Restore from full backup
├─ Replay transaction logs up to target time
└─ Verify data integrity
```

## Scaling Considerations

### Vertical Scaling (For current design)
- Add indexes as query patterns emerge
- Increase connection pool size
- Optimize slow queries

### Horizontal Scaling (Future)
- **Read Replicas**: For reporting/analytics
- **Sharding**: By user_id or product_id
- **Event Streaming**: Kafka for real-time sync

### Archive Strategy
- Move old reservations to archive table
- Keep hot data in main tables
- Reduces table scan time for cleanup job
