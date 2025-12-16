from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from .models import Cart
from .services import add_to_cart
from apps.products.models.variant import Variant

class AddToCartView(APIView):
    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user_id=request.data["user_id"])
        variant = Variant.objects.get(id=request.data["variant_id"])

        add_to_cart(
            cart,
            variant,
            request.data["quantity"],
            request.data["price"]
        )

        return Response({"status": "added"})
