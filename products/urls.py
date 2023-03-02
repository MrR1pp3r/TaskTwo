from django.urls import path
from . import views

urlpatterns = [
    path("product/", views.ProductView.as_view()),
    path("productimage/", views.ProductImageView.as_view()),
]
