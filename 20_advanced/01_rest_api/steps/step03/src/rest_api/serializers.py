from rest_framework import serializers
from .models import Author, Book, Review


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Author
        fields = ['id', 'name', 'bio', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model  = Review
        fields = ['id', 'author', 'rating', 'body', 'created_at']


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.name')
    reviews     = ReviewSerializer(many=True, read_only=True)
    owner       = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model  = Book
        fields = [
            'id', 'title', 'author', 'author_name', 'genre',
            'published', 'description', 'owner', 'reviews', 'created_at',
        ]
