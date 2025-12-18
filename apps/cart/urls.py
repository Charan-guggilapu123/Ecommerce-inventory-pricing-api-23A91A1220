from django.urls import path
from .views import AddToCartView, CheckoutView

urlpatterns = [
    path("add/", AddToCartView.as_view()),
    path("checkout/", CheckoutView.as_view()),
]
