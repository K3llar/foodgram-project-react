from django.contrib import admin
from django.urls import include, path
from djoser.views import TokenCreateView

from .views import CustomTokenDestroyView

app_name = 'users'

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/token/login/', TokenCreateView.as_view(), name='login'),
    path('auth/token/logout/', CustomTokenDestroyView.as_view(), name='logout'),
]
