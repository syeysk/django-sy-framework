from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django_sy_framework.custom_auth.models import CustomAuthUser


admin.site.register(CustomAuthUser, UserAdmin)
