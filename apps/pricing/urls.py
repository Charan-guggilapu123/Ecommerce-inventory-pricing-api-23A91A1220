from django.urls import path
from .views import ProductPriceView

urlpatterns = [
    path("<int:product_id>/price/", ProductPriceView.as_view()),
]
