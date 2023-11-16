from django.contrib.auth import get_user_model
from django.db import models


class Token(models.Model):
    user = models.ForeignKey(get_user_model(), null=False, on_delete=models.CASCADE)
    app_name = models.CharField(verbose_name='Наименование приложения', max_length=20, null=False, blank=False)
    token = models.CharField(
        verbose_name='Токен для доступа к API сервера',
        max_length=128,
        null=False,
        blank=False,
        unique=True,
    )
    expire_dt = models.DateTimeField(verbose_name='Время жизни токена', null=True)

    class Meta:
        verbose_name = 'Токен'
        verbose_name_plural = 'Токены'