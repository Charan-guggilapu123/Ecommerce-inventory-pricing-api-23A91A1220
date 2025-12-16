from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from apps.products.models.product import Product
from .engine import PricingEngine

class ProductPriceView(APIView):
    def get(self, request, product_id):
        qty = int(request.query_params.get("quantity", 1))
        user_tier = request.query_params.get("user_tier")

        product = Product.objects.get(id=product_id)
        engine = PricingEngine()

        price, breakdown = engine.calculate(product.base_price, qty, user_tier)

        return Response({
            "final_price": price,
            "breakdown": breakdown
        })
