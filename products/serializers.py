from .models import Product, ProductImage
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductImageSerialzier(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    product_id = serializers.SerializerMethodField()
    product_desc = serializers.SerializerMethodField()
    product_price = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.product.title

    def get_product_id(self, obj):
        return obj.product.id

    def get_product_desc(self, obj):
        return obj.product.description

    def get_product_price(self, obj):
        return obj.product.price

    class Meta:
        model = ProductImage
        exclude = ("product",)


class ProductImagePSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"
