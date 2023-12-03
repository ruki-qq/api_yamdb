from rest_framework import filters, mixins, viewsets

from api.v1.permissions import IsAdminOrReadOnly


class BaseCatGenrViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
