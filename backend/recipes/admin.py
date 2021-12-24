from django.contrib import admin

from .models import (FavoriteRecipe, Ingredient, Recipe, RecipeIngredients,
                     RecipeTags, ShoppingList, Tag)


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


class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredients
    min_num = 1
    extra = 1


class RecipeTagsInline(admin.TabularInline):
    model = RecipeTags
    min_num = 1
    extra = 0


@admin.register(RecipeTags)
class RecipeTagsAdmin(SiteAdmin):
    list_display = ('id',
                    'recipe',
                    'tag')
    list_filter = ('id', 'recipe', 'tag')


@admin.register(RecipeIngredients)
class RecipeIngredientsAdmin(SiteAdmin):
    list_display = ('id',
                    'recipe',
                    'ingredient',
                    'amount')
    list_filter = ('id', 'recipe', 'ingredient')


@admin.register(Recipe)
class RecipeAdmin(SiteAdmin):
    list_display = ('id',
                    'name',
                    'author',
                    'in_favorite',)
    list_filter = ('name', 'author', 'tags', 'in_favorite')
    inlines = (RecipeTagsInline, RecipeIngredientsInline)

    @staticmethod
    def in_favorite(obj):
        return obj.in_favorite.all().count()


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(SiteAdmin):
    list_display = ('id',
                    'user',
                    'recipe',)


@admin.register(ShoppingList)
class ShoppingListAdmin(SiteAdmin):
    list_display = ('id',
                    'user',
                    'recipe')
