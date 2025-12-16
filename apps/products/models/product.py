from django.db import models
from .category import Category

class Product(models.Model):
    STATUS = (
        ("active", "Active"),
        ("archived", "Archived"),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
