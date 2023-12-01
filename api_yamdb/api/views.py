from pprint import pprint
from django.shortcuts import get_object_or_404
from django_filters import CharFilter, NumberFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import viewsets, permissions, filters, mixins

from reviews.models import (Genre, Category, Title, Review, Comment)
from api.permissions import OwnerOrReadOnly, AdminOrReadOnly
from api.serializers import (GenreSerializer, CategorySerializer, TitleSerializerGET, TitleSerializerPOST, ReviewSerializer, CommentSerializer)

class GenreViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, 
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)

class CategoryViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)


class TitleFilter(FilterSet):
    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genres__genre__slug')
    year = NumberFilter(field_name='year')
    class Meta:
        model = Title
        fields = ('name', 'category', 'genre', 'year')

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    ordering = ['id']
    serializer_class = TitleSerializerGET
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (AdminOrReadOnly,)
    http_method_names = ('get', 'post', 'delete', 'patch',)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializerGET
        return TitleSerializerPOST

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (OwnerOrReadOnly,)
    http_method_names = ('get', 'post', 'delete', 'patch',)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

#    def create(self, request, *args, **kwargs):
#        request.data['title'] = self.get_title()
#        request.data['author'] = self.request.user
#        serializer = self.get_serializer(data=request.data)
#        serializer.is_valid(raise_exception=True)
#        self.perform_create(serializer)

    def perform_create(self, serializer):
        serializer.save(title=self.get_title(), author=self.request.user)



class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (OwnerOrReadOnly,)
    http_method_names = ('get', 'post', 'delete', 'patch',)

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(review=self.get_review(), author=self.request.user) 
