from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


"""
Привет, отличное начало! Давайте теперь причешем весь проект 
(призываю вас вместе пройтись по всему коду, держа в уме все ремарки,
т.к. они относятся более чем к одной строке). Также следует 
добавить модели в админку + прописать verbose_name's и 
определить str по всем моделям.
"""


# поля доступные админу
"""
давайте писать грамотную документацию (по pep-257) - большой проект ведь делаем :) 
Надо исправить
"""
class CustomUserAdmin(UserAdmin):
    list_display = ("pk", "email", "bio", "confirmation_code", "role")


admin.site.register(User, CustomUserAdmin)
"""
Давайте перепишем регистрацию классов админки через декоратор
https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#the-register-decorator 
Можно лучше
"""
