from django.conf import settings
from django.contrib import admin

from .models import Tag, Ingredient


class SiteAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagsAdmin(SiteAdmin):
    list_display = ('id',
                    'name',
                    'color',
                    'slug',)
    search_fields = ('name',)


@admin.register(Ingredient)
class IngredientSerializer(SiteAdmin):
    list_display = ('id',
                    'name',
                    'measurement_unit',)
    search_fields = ('name',)
