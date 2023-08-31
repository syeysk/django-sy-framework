from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Linker(models.Model):
    link_to = models.CharField('Тип объекта, к которому привязываем', max_length=15)
    link_to_id = models.PositiveIntegerField('ID объекта, к которому привязываем')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, help_text='Тип привязанного объекта')
    object_id = models.PositiveIntegerField('ID привязанного объекта')
    content_object = GenericForeignKey()

    class Meta:
        verbose_name = 'Привязанный объект'
        verbose_name_plural = 'Привязанные объекты'
        constraints = [
            models.UniqueConstraint(
                fields=('link_to', 'link_to_id', 'content_type', 'object_id'),
                name='unique_linker',
            ),
        ]
        indexes = [
            models.Index(fields=('content_type', 'object_id'), name='index_content_type_linker'),
        ]
