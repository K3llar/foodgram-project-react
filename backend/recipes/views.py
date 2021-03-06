from django.http import HttpResponse
from django.template.loader import render_to_string
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from weasyprint import HTML

from backend.pagination import CustomPageNumberPaginator

from .filters import IngredientFilter, RecipeFilter
from .models import (FavoriteRecipe, Ingredient, Recipe, RecipeIngredients,
                     ShoppingList, Tag)
from .permissions import AdminOrReadOnly, AuthorOrAdmin
from .serializers import (AddRecipeSerializer, FavoriteRecipeSerializer,
                          IngredientSerializer, ShoppingListSerializer,
                          ShowRecipeSerializer, TagSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (AdminOrReadOnly,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_classes = {
        'retrieve': ShowRecipeSerializer,
        'list': ShowRecipeSerializer,
    }
    default_serializer_class = AddRecipeSerializer
    permission_classes = (AuthorOrAdmin,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = CustomPageNumberPaginator

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action,
                                           self.default_serializer_class)

    @action(detail=True)
    def favorite(self, request, pk):
        data = {'user': request.user.id,
                'recipe': pk}
        serializer = FavoriteRecipeSerializer(data=data,
                                              context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        favorite = get_object_or_404(FavoriteRecipe,
                                     user=user,
                                     recipe=recipe)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True)
    def shopping_cart(self, request, pk):
        data = {'user': request.user.id,
                'recipe': pk}
        serializer = ShoppingListSerializer(data=data,
                                            context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        shopping_list = get_object_or_404(ShoppingList,
                                          user=user,
                                          recipe=recipe)
        shopping_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False)
    def download_shopping_cart(self, request):
        shopping_list = request.user.shopping_list.all()
        ingredients = get_list_of_ingredients(shopping_list)
        html_template = render_to_string('recipes/pdf_template.html',
                                         {'ingredients': ingredients})
        html = HTML(string=html_template)
        result = html.write_pdf()
        response = HttpResponse(result, content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; filename=shopping_list.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        return response


def get_list_of_ingredients(recipe_list):
    ingredients_dict = {}
    for recipe in recipe_list:
        ingredients = RecipeIngredients.objects.filter(recipe=recipe.recipe)
        for ingredient in ingredients:
            amount = ingredient.amount
            name = ingredient.ingredient.name
            measurement_unit = ingredient.ingredient.measurement_unit
            if name not in ingredients_dict:
                ingredients_dict[name] = {
                    'measurement_unit': measurement_unit,
                    'amount': amount,
                }
            else:
                ingredients_dict[name]['amount'] += amount
    return ingredients_dict
