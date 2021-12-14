from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import TagViewSet, IngredientViewSet

app_name = 'recipes'

api_recipes_router = DefaultRouter()
api_recipes_router.register(r'tags', TagViewSet, basename='tags')
api_recipes_router.register(r'ingredients', IngredientViewSet,
                            basename='ingredients')

urlpatterns = [
    path(r'', include(api_recipes_router.urls)),
]
