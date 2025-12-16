from rest_framework.viewsets import ModelViewSet
from apps.products.models.category import Category
from apps.products.serializers.category import CategorySerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
