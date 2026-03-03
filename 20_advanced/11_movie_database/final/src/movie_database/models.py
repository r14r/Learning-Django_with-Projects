from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    def __str__(self): return self.name


class Person(models.Model):
    name       = models.CharField(max_length=200)
    birth_date = models.DateField(null=True, blank=True)
    bio        = models.TextField(blank=True)
    photo      = models.ImageField(upload_to='persons/', blank=True)
    def __str__(self): return self.name


class Movie(models.Model):
    title      = models.CharField(max_length=300)
    slug       = models.SlugField(unique=True)
    year       = models.IntegerField()
    duration   = models.PositiveIntegerField(default=0)
    synopsis   = models.TextField(blank=True)
    poster     = models.ImageField(upload_to='posters/', blank=True)
    director   = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, related_name='directed')
    cast       = models.ManyToManyField(Person, related_name='movies', blank=True)
    genres     = models.ManyToManyField(Genre, blank=True, related_name='movies')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['-year', 'title']
    def __str__(self): return f'{self.title} ({self.year})'
    def get_absolute_url(self): return reverse('movie_database:detail', kwargs={'slug': self.slug})


class Rating(models.Model):
    movie      = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    score      = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: unique_together = ('movie', 'user')


class Review(models.Model):
    movie      = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    author     = models.ForeignKey(User, on_delete=models.CASCADE)
    body       = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['-created_at']


class Watchlist(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    class Meta: unique_together = ('user', 'movie')
