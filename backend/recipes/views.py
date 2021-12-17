from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import (Tag,
                     Ingredient,
                     Recipe,
                     FavoriteRecipe,
                     RecipeTags,
                     RecipeIngredients)
from .serializers import (TagSerializer,
                          IngredientSerializer,
                          ShowRecipeSerializer,
                          AddRecipeSerializer,
                          FavoriteRecipeSerializer,
                          ShowFavoriteRecipeSerializer)
from .permissions import AdminOrReadOnly, AuthorOrAdmin
from .filters import IngredientFilter

from backend.pagination import CustomPageNumberPaginator


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = CustomPageNumberPaginator
    permission_classes = (AdminOrReadOnly,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = CustomPageNumberPaginator
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_classes = {
        'retrieve': ShowRecipeSerializer,
        'list': ShowRecipeSerializer,
    }
    default_serializer_class = AddRecipeSerializer
    permission_classes = (AuthorOrAdmin,)
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = RecipeFilter
    pagination_class = CustomPageNumberPaginator

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

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
