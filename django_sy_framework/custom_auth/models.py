from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomAuthUser(AbstractUser):
    microservice_auth_id = models.UUIDField(null=False, blank=False, unique=True)

    class Meta(AbstractUser.Meta):
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class TempTokenModel(models.Model):
    user_hash = models.CharField(max_length=32, null=False, blank=False)
    temp_token = models.CharField(max_length=32, null=False, blank=False)
    public_key = models.TextField(max_length=10000, null=False, blank=False)
    private_key = models.TextField(max_length=10000, null=False, blank=False)
    auth_public_key = models.TextField(max_length=10000, null=False, blank=False)
