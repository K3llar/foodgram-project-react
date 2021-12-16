from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import TagViewSet, IngredientViewSet, RecipeViewSet

app_name = 'recipes'

api_recipes_router = DefaultRouter()
api_recipes_router.register(r'tags', TagViewSet, basename='tags')
api_recipes_router.register(r'ingredients', IngredientViewSet,
                            basename='ingredients')
api_recipes_router.register(r'recipes', RecipeViewSet,
                            basename='recipes')

urlpatterns = [
    path(r'', include(api_recipes_router.urls)),
]
