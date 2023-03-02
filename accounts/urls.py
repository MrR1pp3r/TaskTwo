from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.CreateView.as_view()),
    path("login/<email>/", views.LoginView.as_view()),
    path("cart/", views.CartView.as_view()),
]
