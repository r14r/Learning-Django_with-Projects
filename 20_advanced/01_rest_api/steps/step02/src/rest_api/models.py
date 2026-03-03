from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Author(models.Model):
    name       = models.CharField(max_length=200)
    bio        = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title       = models.CharField(max_length=300)
    author      = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    genre       = models.CharField(max_length=100)
    published   = models.IntegerField()
    description = models.TextField(blank=True)
    cover       = models.ImageField(upload_to='covers/', blank=True)
    owner       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Review(models.Model):
    book       = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    author     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating     = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    body       = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('book', 'author')
        ordering        = ['-created_at']

    def __str__(self):
        return f'{self.author.username} on {self.book.title}'
