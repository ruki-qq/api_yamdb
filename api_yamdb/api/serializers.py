from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField, StringRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Genre, Category, Title, Review, Comment


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Genre
        lookup_field = 'slug'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Category
        lookup_field = 'slug'

class TitleSerializerGET(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()


    class Meta:
        fields = '__all__'
        model = Title


    def get_rating(self, obj):
        rating = obj.reviews.all().aggregate(Avg('score'))['score__avg']
        if rating:
            return int(rating)
        else:
            return None

class TitleSerializerPOST(serializers.ModelSerializer):
    category = SlugRelatedField(slug_field='slug', queryset=Category.objects.all())
    genre = SlugRelatedField(slug_field='slug', queryset=Genre.objects.all(), many=True)


    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = StringRelatedField(read_only=True, default=serializers.CurrentUserDefault())
#    title = StringRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title', 'author',)
#        validators = (UniqueTogetherValidator(
#                      queryset=Review.objects.all(), fields=('title', 'author')),)

class CommentSerializer(serializers.ModelSerializer):
    author = StringRelatedField(read_only=True)
    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review', 'author',)
