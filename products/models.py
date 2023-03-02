from uuid import uuid4

from django.db import models


# Create your models here.
class Product(models.Model):
    product_id = models.CharField(default=uuid4, max_length=522)
    title = models.CharField(max_length=254, blank=False, unique=True)
    description = models.CharField(max_length=1024)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return f"{self.title} with {self.price}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_img = models.ImageField(upload_to="media/product/")
