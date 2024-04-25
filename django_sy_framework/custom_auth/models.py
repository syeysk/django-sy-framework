from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_sy_framework.custom_auth.validators import UnicodeUsernameValidator


class CustomAuthUser(AbstractUser):
    USERNAME_FIELD = 'microservice_auth_id'
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and ./+/-/_ only.'),
        validators=[username_validator],
    )
    microservice_auth_id = models.UUIDField(null=False, blank=False, unique=True)

    def __str__(self):
        return f'<{self.microservice_auth_id}> {self.username}'

    class Meta(AbstractUser.Meta):
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class TempTokenModel(models.Model):
    user_hash = models.CharField(max_length=32, null=False, blank=False)
    temp_token = models.CharField(max_length=32, null=False, blank=False)
    public_key = models.TextField(max_length=10000, null=False, blank=False)
    private_key = models.TextField(max_length=10000, null=False, blank=False)
    auth_public_key = models.TextField(max_length=10000, null=False, blank=False)
