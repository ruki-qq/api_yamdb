from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Genre, Category, Title, Review, Comment


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genre
        lookup_field = 'slug'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Category
        lookup_field = 'slug'

class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Title

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Review

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Comment
