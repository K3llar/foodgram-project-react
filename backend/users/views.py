from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

from rest_framework import status, viewsets, permissions, filters, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from djoser import utils
from djoser.views import TokenDestroyView
from rest_framework.views import APIView

from backend.pagination import CustomPageNumberPaginator

from .serializers import FollowSerializer
from .models import Follow, User


class CustomTokenDestroyView(TokenDestroyView):

    def post(self, request):
        utils.logout_user(request)
        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE'])
@permission_classes([permissions.IsAuthenticated, ])
def follow_author(request, pk):
    user = get_object_or_404(User, username=request.user.username)
    author = get_object_or_404(User, pk=pk)

    if request.method == 'GET':
        if user.id == author.id:
            content = {'errors': 'Нельзя подписаться на свой канал'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            Follow.objects.create(user=user, author=author)
        except IntegrityError:
            content = {'errors': 'Вы уже подписаны на данного автора'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        follows = User.objects.all().filter(username=author)
        serializer = FollowSerializer(follows,
                                      context={'request': request},
                                      many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    if request.method == 'DELETE':
        try:
            obj = Follow.objects.get(user=user, author=author)
        except ObjectDoesNotExist:
            content = {'errors': 'Вы не подписаны на данного автора'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        obj.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class FollowListViewSet(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = FollowSerializer
    pagination_class = CustomPageNumberPaginator
    filter_backends = (filters.SearchFilter,)
    permission_classes = (permissions.IsAuthenticated,)
    search_fields = ('^following__user',)

    def get_queryset(self):
        user = self.request.user
        new_queryset = User.objects.filter(following__user=user)
        return new_queryset
