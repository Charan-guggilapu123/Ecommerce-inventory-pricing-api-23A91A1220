"""
E-commerce API Testing Script
Tests all endpoints to verify the system is working correctly
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_endpoint(method, url, data=None, expected_status=200, description=""):
    """Helper function to test endpoints"""
    print(f"\n{'='*60}")
    print(f"TEST: {description}")
    print(f"{'='*60}")
    print(f"{method} {url}")
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
        elif method == "PUT":
            response = requests.put(url, json=data, headers={"Content-Type": "application/json"})
        elif method == "DELETE":
            response = requests.delete(url)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == expected_status:
            print("✅ SUCCESS")
        else:
            print(f"❌ FAILED - Expected {expected_status}, got {response.status_code}")
        
        try:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return response.json()
        except:
            print(f"Response: {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return None

# Test 1: Create Category
print("\n" + "="*60)
print("STEP 1: CREATE CATEGORY")
print("="*60)
category = test_endpoint(
    "POST", 
    f"{BASE_URL}/products/categories/",
    {"name": "Clothing"},
    201,
    "Create Clothing Category"
)

# Test 2: List Categories
test_endpoint(
    "GET",
    f"{BASE_URL}/products/categories/",
    description="List all categories"
)

# Test 3: Create Product
print("\n" + "="*60)
print("STEP 2: CREATE PRODUCT")
print("="*60)
product = test_endpoint(
    "POST",
    f"{BASE_URL}/products/",
    {
        "name": "T-Shirt",
        "description": "Black cotton t-shirt",
        "base_price": "500.00",
        "status": "active",
        "category": category['id'] if category else 1
    },
    201,
    "Create T-Shirt Product"
)

# Test 4: List Products
test_endpoint(
    "GET",
    f"{BASE_URL}/products/",
    description="List all products"
)

# Test 5: Get Product Detail
if product:
    test_endpoint(
        "GET",
        f"{BASE_URL}/products/{product['id']}/",
        description=f"Get product {product['id']} details"
    )

print("\n" + "="*60)
print("ALL TESTS COMPLETED")
print("="*60)
