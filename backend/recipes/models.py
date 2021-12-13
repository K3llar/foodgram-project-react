from django.db import models
from django.utils.translation import gettext_lazy as _

from .fields import HexColorField


class Tag(models.Model):
    name = models.CharField(verbose_name=_('Название'),
                            max_length=40,
                            unique=True)
    color = HexColorField(verbose_name=_('Цветовой HEX-код'),
                          unique=True)
    slug = models.SlugField(verbose_name=_('Короткое наименование'),
                            unique=True)
    REQUIRED_FIELDS = ('name',
                       'color',
                       'slug',)

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ('-id',)
        verbose_name_plural = 'Идентификаторы'
