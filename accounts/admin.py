from django.contrib import admin
from .models import UserloginotpModel, User, UserCartModel, UserCartProductModel, UserProfileModel

# Register your models here.

admin.site.register(User)
admin.site.register(UserloginotpModel)
admin.site.register(UserCartModel)
admin.site.register(UserProfileModel)
admin.site.register(UserCartProductModel)
