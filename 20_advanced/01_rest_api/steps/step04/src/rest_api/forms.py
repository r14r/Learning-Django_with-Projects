from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Author, Book, Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.name')
    owner       = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model  = Book
        fields = [
            'id', 'title', 'author', 'author_name', 'genre',
            'published', 'description', 'owner', 'created_at',
        ]