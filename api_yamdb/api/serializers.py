from django.db.models import Avg
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
    category = SlugRelatedField(slug_field='slug', queryset=Category.objects.all())
    genre = SlugRelatedField(slug_field='slug', queryset=Genre.objects.all(), many=True)
    rating = serializers.SerializerMethodField()


    class Meta:
        fields = '__all__'
        model = Title


    def get_rating(self, obj):
        rating = obj.reviews.all().aggregate(Avg('score'))['score__avg']
        if rating:
            return int(rating)
        else:
            return 0

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Review

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Comment
