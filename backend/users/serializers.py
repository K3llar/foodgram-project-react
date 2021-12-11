from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.fields import CurrentUserDefault

from .models import Follow

User = get_user_model()


class CurrentUserDefaultId(object):
    requires_context = True

    def __call__(self, serializer_instance=None):
        if serializer_instance is not None:
            self.user_id = serializer_instance.context['request'].user.id
            return self.user_id


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=self.context['request'].user,
                                     author=obj).exists()


class FollowSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if not user:
            return False
        return Follow.objects.filter(user=user, author=obj).exists()

    def get_recipes(self, obj):
        pass

    def get_recipes_count(self, obj):
        pass

# class FollowSerializer(serializers.ModelSerializer):
#     user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
#     author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
#
#     class Meta:
#         model = Follow
#         fields = ('user', 'author')
#
#     def validate(self, data):
#         user = self.context.get('request').user
#         author_id = data['author'].id
#         if Follow.objects.filter(user=user,
#                                  author__id=author_id).exists():
#             raise serializers.ValidationError(
#                     'Вы уже подписаны на этого пользователя')
#         if user.id == author_id:
#             raise serializers.ValidationError('Нельзя подписаться на себя')
#         return data
