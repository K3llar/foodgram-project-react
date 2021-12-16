from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import (Tag,
                     Ingredient,
                     Recipe,
                     RecipeTags,
                     RecipeIngredients)
from .serializers import (TagSerializer,
                          IngredientSerializer,
                          # RecipeSerializer,
                          ShowRecipeSerializer)
from .permissions import AdminOrReadOnly


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = PageNumberPagination
    permission_classes = (AdminOrReadOnly,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = PageNumberPagination


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = ShowRecipeSerializer
    pagination_class = PageNumberPagination
