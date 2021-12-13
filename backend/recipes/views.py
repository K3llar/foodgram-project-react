from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Tag
from .serializers import TagSerializer
from .permissions import AdminOrReadOnly


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = PageNumberPagination
    permission_classes = (AdminOrReadOnly,)
