from django.conf import settings
from django.contrib import admin

from .models import Tag


class SiteAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagsAdmin(SiteAdmin):
    list_display = ('id',
                    'name',
                    'color',
                    'slug',)
    search_fields = ('name',)
