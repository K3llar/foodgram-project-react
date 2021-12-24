from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .fields import HexColorField

User = get_user_model()


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


class Ingredient(models.Model):
    name = models.CharField(verbose_name=_('Название'),
                            max_length=200)
    measurement_unit = models.CharField(
        verbose_name=_('Единица измерения'),
        max_length=50,
    )
    REQUIRED_FIELDS = ('name',
                       'measurement_unit',)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Ингредиенты'
        constraints = (
            models.UniqueConstraint(fields=('name',
                                            'measurement_unit'),
                                    name='pair_unique'),
        )


class Recipe(models.Model):
    name = models.CharField(verbose_name=_('Название'),
                            max_length=200, )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name=_('Автор рецепта'))
    text = models.TextField(verbose_name=_('Описание'))
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTags',
        verbose_name=_('Идентификаторы рецепта'),
        related_name='recipes',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredients',
        verbose_name=_('Ингредиенты рецепта'),
        related_name='recipes',
    )
    image = models.ImageField(upload_to='recipes/')
    cooking_time = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1),),
        verbose_name=_('Время готовки'))

    REQUIRED_FIELDS = '__all__'

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeTags(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name=_('Идентификатор рецептов'), )
    tag = models.ForeignKey(Tag,
                            on_delete=models.CASCADE,
                            verbose_name=_('Идентификатор'))

    class Meta:
        verbose_name = 'Идентификатор рецепта'
        verbose_name_plural = 'Идентификаторы рецептов'


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name=_('Ингредиент рецептов'))
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.PROTECT,
                                   verbose_name=_('Ингредиент'), )
    amount = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1),),
        verbose_name=_('Количество'),
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'


class FavoriteRecipe(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name=_('Рецепт'),
                               related_name='in_favorite')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name=_('Пользователь'),
                             related_name='favorite')

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=('recipe',
                                            'user'),
                                    name='pair_unique_favorite'),
        )
        ordering = ('-id',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные рецепты'


class ShoppingList(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name=_('Рецепт'),
                               related_name='recipe_in_cart')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name=_('Пользователь'),
                             related_name='shopping_list')

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=('recipe',
                                            'user'),
                                    name='pair_unique_shopping'),
        )
        ordering = ('-id',)
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
