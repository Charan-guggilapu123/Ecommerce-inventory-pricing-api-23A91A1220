# API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication
Currently, no authentication required. JWT authentication can be added by extending the ViewSets.

---

## Endpoints Reference

### Categories API

#### 1. List All Categories
```
GET /api/products/categories/
```

**Description**: Retrieve all product categories with hierarchical structure

**Query Parameters**:
| Parameter | Type | Optional | Description |
|-----------|------|----------|-------------|
| page | integer | Yes | Page number (pagination) |
| limit | integer | Yes | Results per page |

**Response (200 OK)**:
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Clothing",
      "description": "Apparel items",
      "parent_id": null,
      "children": [
        {
          "id": 2,
          "name": "Men's Clothing",
          "description": "Men's apparel",
          "parent_id": 1,
          "children": []
        }
      ]
    }
  ]
}
```

**Error Responses**:
- `500 Internal Server Error`: Database connection failed

---

#### 2. Create Category
```
POST /api/products/categories/
```

**Description**: Create a new product category

**Request Body**:
```json
{
  "name": "Electronics",
  "description": "Electronic devices and accessories",
  "parent_id": null
}
```

**Request Schema**:
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| name | string | Yes | Max 255 chars, unique |
| description | string | No | Optional |
| parent_id | integer | No | Must reference existing category |

**Response (201 Created)**:
```json
{
  "id": 3,
  "name": "Electronics",
  "description": "Electronic devices and accessories",
  "parent_id": null,
  "children": []
}
```

**Error Responses**:
```
400 Bad Request
{
  "name": ["This field is required."]
}

409 Conflict
{
  "name": ["Category with this name already exists."]
}
```

---

#### 3. Get Category Details
```
GET /api/products/categories/{id}/
```

**Description**: Retrieve a specific category with its subcategories

**URL Parameters**:
| Parameter | Type | Required |
|-----------|------|----------|
| id | integer | Yes |

**Response (200 OK)**:
```json
{
  "id": 1,
  "name": "Clothing",
  "description": "Apparel items",
  "parent_id": null,
  "children": [
    {
      "id": 2,
      "name": "Men",
      "description": "Men's clothing",
      "parent_id": 1,
      "children": []
    },
    {
      "id": 3,
      "name": "Women",
      "description": "Women's clothing",
      "parent_id": 1,
      "children": []
    }
  ]
}
```

**Error Responses**:
- `404 Not Found`: Category doesn't exist

---

### Products API

#### 1. List All Products
```
GET /api/products/
```

**Description**: Retrieve all products with pagination

**Query Parameters**:
| Parameter | Type | Optional | Description |
|-----------|------|----------|-------------|
| page | integer | Yes | Page number (default: 1) |
| category | integer | Yes | Filter by category ID |

**Response (200 OK)**:
```json
{
  "count": 2,
  "next": "http://localhost:8000/api/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "T-Shirt",
      "category": 1,
      "category_name": "Clothing",
      "base_price": "500.00",
      "variants": [
        {
          "id": 1,
          "sku": "TSHIRT-BLK-M",
          "price_adjustment": "50.00"
        }
      ],
      "created_at": "2025-12-17T10:30:00Z",
      "updated_at": "2025-12-17T10:30:00Z"
    }
  ]
}
```

---

#### 2. Create Product
```
POST /api/products/
```

**Description**: Create a new product

**Request Body**:
```json
{
  "name": "Jeans",
  "category": 1,
  "description": "Classic blue jeans",
  "base_price": "800.00"
}
```

**Request Schema**:
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| name | string | Yes | Max 255 chars |
| category | integer | Yes | Must reference existing category |
| description | string | No | Optional |
| base_price | decimal | Yes | > 0, 2 decimal places |

**Response (201 Created)**:
```json
{
  "id": 2,
  "name": "Jeans",
  "category": 1,
  "category_name": "Clothing",
  "base_price": "800.00",
  "variants": [],
  "created_at": "2025-12-17T10:35:00Z",
  "updated_at": "2025-12-17T10:35:00Z"
}
```

**Error Responses**:
```
400 Bad Request
{
  "base_price": ["Ensure this value is greater than or equal to 0.01."],
  "category": ["This field is required."]
}

404 Not Found
{
  "detail": "Category not found"
}
```

---

### Variants API

#### 1. List All Variants
```
GET /api/products/variants/
```

**Description**: Retrieve all product variants

**Query Parameters**:
| Parameter | Type | Optional | Description |
|-----------|------|----------|-------------|
| product | integer | Yes | Filter by product ID |
| sku | string | Yes | Filter by SKU |

**Response (200 OK)**:
```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "product": 1,
      "sku": "TSHIRT-BLK-M",
      "attributes": {
        "color": "black",
        "size": "M"
      },
      "price_adjustment": "50.00",
      "is_active": true,
      "created_at": "2025-12-17T10:40:00Z"
    }
  ]
}
```

---

#### 2. Create Variant
```
POST /api/products/variants/
```

**Description**: Create a product variant (SKU)

**Request Body**:
```json
{
  "product": 1,
  "sku": "TSHIRT-RED-L",
  "attributes": {
    "color": "red",
    "size": "L"
  },
  "price_adjustment": "50.00"
}
```

**Request Schema**:
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| product | integer | Yes | Must reference existing product |
| sku | string | Yes | Unique, max 255 chars |
| attributes | object | No | JSON object for flexibility |
| price_adjustment | decimal | No | Default: 0, can be positive or negative |
| is_active | boolean | No | Default: true |

**Response (201 Created)**:
```json
{
  "id": 2,
  "product": 1,
  "sku": "TSHIRT-RED-L",
  "attributes": {
    "color": "red",
    "size": "L"
  },
  "price_adjustment": "50.00",
  "is_active": true,
  "created_at": "2025-12-17T10:42:00Z"
}
```

**Error Responses**:
```
400 Bad Request
{
  "sku": ["Variant with this SKU already exists."]
}

404 Not Found
{
  "detail": "Product not found"
}
```

---

### Pricing API

#### Calculate Product Price
```
GET /api/pricing/{product_id}/price/
```

**Description**: Calculate final price with all applicable rules

**URL Parameters**:
| Parameter | Type | Required |
|-----------|------|----------|
| product_id | integer | Yes |

**Query Parameters**:
| Parameter | Type | Optional | Description |
|-----------|------|----------|-------------|
| quantity | integer | Yes | Number of units (default: 1) |
| variant_id | integer | Yes | Specific variant (applies price adjustment) |
| user_tier | string | Yes | STANDARD, GOLD, PLATINUM (default: STANDARD) |

**Example Requests**:
```bash
# Basic: 1 unit, standard tier
GET /api/pricing/1/price/

# With quantity and tier
GET /api/pricing/1/price/?quantity=10&user_tier=GOLD

# With specific variant
GET /api/pricing/1/price/?quantity=5&variant_id=1&user_tier=PLATINUM
```

**Response (200 OK)**:
```json
{
  "product_id": 1,
  "base_price": 500.00,
  "quantity": 10,
  "user_tier": "GOLD",
  "pricing_breakdown": {
    "base_price": 500.00,
    "variant_adjustment": 50.00,
    "subtotal_per_unit": 550.00,
    "quantity_discount_percent": 10,
    "quantity_discount_amount": 55.00,
    "after_quantity_discount": 495.00,
    "tier_discount_percent": 15,
    "tier_discount_amount": 74.25,
    "final_price_per_unit": 420.75
  },
  "final_price_total": 4207.50,
  "currency": "USD"
}
```

**Pricing Rules Applied** (in order):
1. **Base Price**: From product table
2. **Variant Adjustment**: Add/subtract variant-specific price
3. **Quantity Discount**:
   - 10-49 units: 10% off
   - 50-99 units: 15% off
   - 100+ units: 20% off
4. **User Tier Discount**:
   - STANDARD: 0%
   - GOLD: 15% off
   - PLATINUM: 25% off

**Error Responses**:
```
404 Not Found
{
  "detail": "Product not found"
}

400 Bad Request
{
  "quantity": ["Quantity must be a positive integer."],
  "user_tier": ["Invalid tier. Choose from: STANDARD, GOLD, PLATINUM"]
}
```

---

### Cart API

#### 1. Get Cart
```
GET /api/cart/
```

**Description**: Retrieve current user's cart with all items

**Query Parameters**:
| Parameter | Type | Optional | Description |
|-----------|------|----------|-------------|
| user_id | integer | Yes | User identifier |

**Response (200 OK)**:
```json
{
  "id": 1,
  "user_id": 123,
  "items": [
    {
      "id": 1,
      "product": 1,
      "product_name": "T-Shirt",
      "quantity": 2,
      "price_snapshot": "420.75",
      "subtotal": "841.50",
      "created_at": "2025-12-17T11:00:00Z"
    },
    {
      "id": 2,
      "product": 2,
      "product_name": "Jeans",
      "quantity": 1,
      "price_snapshot": "750.00",
      "subtotal": "750.00",
      "created_at": "2025-12-17T11:02:00Z"
    }
  ],
  "total_items": 2,
  "cart_total": "1591.50",
  "created_at": "2025-12-17T10:55:00Z",
  "updated_at": "2025-12-17T11:02:00Z"
}
```

---

#### 2. Add Item to Cart
```
POST /api/cart/items/
```

**Description**: Add a product to the shopping cart

**Request Body**:
```json
{
  "cart_id": 1,
  "product": 1,
  "variant_id": 1,
  "quantity": 2,
  "user_tier": "GOLD"
}
```

**Request Schema**:
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| cart_id | integer | Yes | Cart must exist |
| product | integer | Yes | Product must exist |
| variant_id | integer | No | Optional, specific variant |
| quantity | integer | Yes | > 0, ≤ available inventory |
| user_tier | string | No | STANDARD/GOLD/PLATINUM |

**Response (201 Created)**:
```json
{
  "id": 1,
  "cart_id": 1,
  "product": 1,
  "product_name": "T-Shirt",
  "quantity": 2,
  "price_snapshot": "420.75",
  "subtotal": "841.50",
  "created_at": "2025-12-17T11:00:00Z"
}
```

**Error Responses**:
```
400 Bad Request
{
  "quantity": ["Insufficient inventory. Available: 5, Requested: 10"]
}

404 Not Found
{
  "detail": "Product not found"
}

409 Conflict
{
  "detail": "Item already in cart. Use PUT to update quantity."
}
```

---

#### 3. Remove Item from Cart
```
DELETE /api/cart/items/{item_id}/
```

**Description**: Remove an item from the cart

**URL Parameters**:
| Parameter | Type | Required |
|-----------|------|----------|
| item_id | integer | Yes |

**Response (204 No Content)**:
```
(Empty response body)
```

**Error Responses**:
- `404 Not Found`: CartItem doesn't exist

---

#### 4. Checkout (Create Reservation)
```
POST /api/cart/checkout/
```

**Description**: Complete checkout and create inventory reservation

**Request Body**:
```json
{
  "cart_id": 1,
  "user_id": 123,
  "user_tier": "GOLD"
}
```

**Request Schema**:
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| cart_id | integer | Yes | Cart must exist and have items |
| user_id | integer | Yes | User identifier |
| user_tier | string | No | STANDARD/GOLD/PLATINUM |

**Response (201 Created)**:
```json
{
  "reservation_id": 1,
  "user_id": 123,
  "status": "ACTIVE",
  "expires_at": "2025-12-17T12:05:00Z",
  "items_reserved": 2,
  "cart_total": "1591.50",
  "message": "Checkout successful. Reservation expires in 5 minutes.",
  "created_at": "2025-12-17T12:00:00Z"
}
```

**Checkout Process**:
1. **Validate**: Cart exists and has items
2. **Lock**: Acquire SELECT FOR UPDATE on inventory rows
3. **Check**: Verify sufficient stock for all items
4. **Reserve**: Update reserved_quantity in inventory
5. **Create**: Insert reservation with 5-minute TTL
6. **Clean**: Delete cart and cart items
7. **Commit**: ACID transaction ensures consistency

**Error Responses**:
```
400 Bad Request
{
  "detail": "Cart is empty or items are out of stock"
}

409 Conflict
{
  "detail": "Inventory locked. Another user checking out. Please retry."
}

500 Internal Server Error
{
  "detail": "Checkout failed. Transaction rolled back. Cart preserved."
}
```

---

## Error Handling

### Standard Error Response Format
```json
{
  "detail": "Human-readable error message",
  "error_code": "ERROR_CODE",
  "timestamp": "2025-12-17T12:00:00Z"
}
```

### HTTP Status Codes
| Code | Meaning | When |
|------|---------|------|
| 200 | OK | Request succeeded |
| 201 | Created | Resource created |
| 204 | No Content | Deletion succeeded |
| 400 | Bad Request | Invalid input |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Resource conflict (SKU exists, lock contention) |
| 500 | Internal Error | Server error, transaction rolled back |

---

## Request/Response Examples

### Example 1: Complete Purchase Workflow

**Step 1: Create Category**
```bash
curl -X POST http://localhost:8000/api/products/categories/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Clothing",
    "description": "Apparel items"
  }'

# Response: 201 Created
# {
#   "id": 1,
#   "name": "Clothing",
#   ...
# }
```

**Step 2: Create Product**
```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "T-Shirt",
    "category": 1,
    "base_price": "500.00"
  }'

# Response: 201 Created
# {
#   "id": 1,
#   "name": "T-Shirt",
#   ...
# }
```

**Step 3: Create Variant**
```bash
curl -X POST http://localhost:8000/api/products/variants/ \
  -H "Content-Type: application/json" \
  -d '{
    "product": 1,
    "sku": "TSHIRT-BLK-M",
    "price_adjustment": "50.00",
    "attributes": {"color": "black", "size": "M"}
  }'

# Response: 201 Created
```

**Step 4: Check Price**
```bash
curl -X GET "http://localhost:8000/api/pricing/1/price/?quantity=10&user_tier=GOLD"

# Response: 200 OK
# {
#   "final_price_total": 4207.50,
#   "final_price_per_unit": 420.75,
#   ...
# }
```

**Step 5: Add to Cart**
```bash
curl -X POST http://localhost:8000/api/cart/items/ \
  -H "Content-Type: application/json" \
  -d '{
    "cart_id": 1,
    "product": 1,
    "quantity": 2,
    "user_tier": "GOLD"
  }'

# Response: 201 Created
```

**Step 6: Checkout**
```bash
curl -X POST http://localhost:8000/api/cart/checkout/ \
  -H "Content-Type: application/json" \
  -d '{
    "cart_id": 1,
    "user_id": 123,
    "user_tier": "GOLD"
  }'

# Response: 201 Created
# {
#   "reservation_id": 1,
#   "status": "ACTIVE",
#   "expires_at": "2025-12-17T12:05:00Z",
#   ...
# }
```

---

## Performance Considerations

### Response Times
- **GET /products/**: ~50ms (with 1000 products)
- **GET /pricing/**: ~30ms (calculation intensive)
- **POST /cart/checkout/**: ~200-500ms (locks + multiple inserts)
- **Concurrent checkouts**: Queued by database locks

### Rate Limiting
Currently not implemented. Can be added using:
- `django-ratelimit`
- `djangorestframework-throttling`

### Caching Strategy
- Category list: Cache 1 hour (invalidate on update)
- Product pricing: Cache 5 minutes
- Cart contents: No cache (real-time)

---

## Testing the API

### Using cURL
```bash
# Get all products
curl http://localhost:8000/api/products/

# Create category
curl -X POST http://localhost:8000/api/products/categories/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Category"}'
```

### Using Python Requests
```python
import requests

# Get pricing
response = requests.get(
    'http://localhost:8000/api/pricing/1/price/',
    params={'quantity': 10, 'user_tier': 'GOLD'}
)
print(response.json())

# Add to cart
response = requests.post(
    'http://localhost:8000/api/cart/items/',
    json={'cart_id': 1, 'product': 1, 'quantity': 2}
)
print(response.status_code, response.json())
```

### Using Postman
1. Import collection from: `postman_collection.json`
2. Set environment variables (base URL, user IDs)
3. Run test suite for full workflow

---

## API Versioning

Current version: **v1**

All endpoints are currently under `/api/` without version prefix.

Future versioning strategy:
- `/api/v1/products/` - Version 1
- `/api/v2/products/` - Version 2 (breaking changes)
- Maintain backward compatibility for 2 major versions
