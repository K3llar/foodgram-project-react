from django.contrib import admin
from django.urls import include, path
from djoser.views import TokenCreateView

from rest_framework.routers import DefaultRouter

from .views import CustomTokenDestroyView, follow_author, FollowListViewSet

app_name = 'users'

api_router = DefaultRouter()
api_router.register(r'users/subscriptions', FollowListViewSet, basename='подписки')

urlpatterns = [
    path('users/<int:pk>/subscribe/',
         follow_author, name='follow-author'),
    path(r'', include(api_router.urls)),
    # path('users/subscriptions/',
    #      FollowListViewSet.as_view(), name='follows'),
    path('', include('djoser.urls')),
    path('auth/token/login/', TokenCreateView.as_view(), name='login'),
    path('auth/token/logout/', CustomTokenDestroyView.as_view(), name='logout'),
]
