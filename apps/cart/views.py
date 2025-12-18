from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart
from .services import add_to_cart, checkout
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

class CheckoutView(APIView):
    def post(self, request):
        try:
            # In a real app, we'd get user from request.user
            user_id = request.data.get("user_id")
            if not user_id:
                return Response({"error": "user_id required"}, status=status.HTTP_400_BAD_REQUEST)

            cart = Cart.objects.get(user_id=user_id)
            checkout(cart)
            return Response({"status": "checkout successful", "message": "Inventory updated"}, status=status.HTTP_200_OK)
            
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Checkout failed", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
