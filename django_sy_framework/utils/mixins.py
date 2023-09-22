from django.db import models


class DatetimeMixin(models.Model):
    dt_create = models.DateTimeField(auto_now_add=True)
    dt_modify = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
