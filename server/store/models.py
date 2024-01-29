from collections.abc import Iterable
from django.db import models

from core.models import BaseModel


# Create your models here.
class Category(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    products: models.Manager["Product"]

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name


class Product(BaseModel):
    category_id: int
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    # tags: "models.JSONField[list[str]]" = models.JSONField(default=list)
    tags = models.TextField(default="")

    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    images: models.Manager["ProductImage"]

    def __str__(self) -> str:
        return self.name


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    product_id: int
    image = models.ImageField(upload_to="product_images/")
    # set processed to false on every image change
    # a task will be run in the background to resize and compress the image
    processed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
