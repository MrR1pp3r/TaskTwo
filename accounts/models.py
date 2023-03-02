from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

from products.models import Product


class CustomManager(BaseUserManager):
    def create_user(self, email=None, phone=None, password=None, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **kwargs)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, phone=None, password=None, **kwargs):
        kwargs.setdefault("is_customer", False)
        kwargs.setdefault("is_admin", True)
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        return self.create_user(email, phone, password, **kwargs)


class User(AbstractUser):
    username = None
    phone = models.CharField(max_length=40, unique=True)
    email = models.EmailField(_("Email Address"), unique=True)
    is_customer = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]

    def __str__(self):
        return self.email


genders = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Others", "Others"),
)


class UserProfileModel(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    dob = models.DateField()
    gender = models.CharField(max_length=8, choices=genders, default="Male")
    image = models.ImageField(upload_to="media/profile/image/")

    def __str__(self):
        return self.name


class UserloginotpModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.PositiveSmallIntegerField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.active}"


cart_status = (
    ("pending", "Pending"),
    ("completed", "Completed"),
)


class UserCartProductModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=cart_status)

    def __str__(self):
        return f"{self.owner.email} with {self.status}."


class UserCartModel(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
