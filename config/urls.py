from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/products/", include("apps.products.urls")),
    path("api/variants/", include("apps.products.urls_variants")),
    path("api/categories/", include("apps.products.urls_categories")),
    path("api/pricing/", include("apps.pricing.urls")),
    path("api/cart/", include("apps.cart.urls")),
]
