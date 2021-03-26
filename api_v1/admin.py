from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


# поля доступные админу
class CustomUserAdmin(UserAdmin):
    list_display = ("pk", "email", "bio", "confirmation_code", "role")


admin.site.register(User, CustomUserAdmin)
