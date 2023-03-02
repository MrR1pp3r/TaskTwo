from rest_framework import serializers
from django.contrib.auth import get_user_model

from products.serializers import ProductSerializer
from .models import UserCartModel

User = get_user_model()


class AllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "phone",
            "email",
        )


class CartSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = UserCartModel
        fields = "__all__"


class CartPSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCartModel
        exclude = ("total_price",)
