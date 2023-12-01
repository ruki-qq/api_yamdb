from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField, StringRelatedField

from reviews.models import Category, Comment, Genre, Review, Title


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ['id']
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['id']
        lookup_field = 'slug'


class TitleSerializerGET(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = '__all__'

    @staticmethod
    def get_rating(obj):
        rating = obj.reviews.all().aggregate(Avg('score'))['score__avg']
        if rating:
            return int(rating)
        return None


class TitleSerializerPOST(serializers.ModelSerializer):
    category = SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = '__all__'

    def to_representation(self, title):
        serializer = TitleSerializerGET(title)
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer):
    author = StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['author', 'title']

    def validate(self, data):
        request = self.context.get('request')

        if request.method != 'POST':
            return data

        if Review.objects.filter(
            author=request.user,
            title=self.context.get('view').kwargs.get('title_id'),
        ).exists():
            raise serializers.ValidationError(
                'You have already reviewed this item.'
            )

        return data


class CommentSerializer(serializers.ModelSerializer):
    author = StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author', 'review']
