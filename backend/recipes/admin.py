from django.conf import settings
from django.contrib import admin

from .models import (Tag,
                     Ingredient,
                     Recipe,
                     RecipeTags,
                     RecipeIngredients,
                     FavoriteRecipe)


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
class IngredientAdmin(SiteAdmin):
    list_display = ('id',
                    'name',
                    'measurement_unit',)
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(SiteAdmin):
    list_display = ('id',
                    'name',
                    'author',
                    'in_favorite',)
    list_filter = ('name', 'author', 'in_favorite')

    # def in_favorite(self, obj):
    #     return obj.in_favorite.all().count()

    @staticmethod
    def in_favorite(obj):
        return obj.in_favorite.all().count()


class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredients
    min_num = 1
    extra = 1


class RecipeTagsInline(admin.TabularInline):
    model = RecipeTags
    min_num = 1
    extra = 0


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(SiteAdmin):
    list_display = ('id',
                    'user',
                    'recipe',)
