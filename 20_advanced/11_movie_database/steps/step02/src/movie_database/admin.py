from django.contrib import admin
from .models import Genre, Person, Movie, Rating, Review, Watchlist

admin.site.register(Genre)
admin.site.register(Person)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'director')
    search_fields = ('title',)
    filter_horizontal = ('cast', 'genres')

admin.site.register(Rating)
admin.site.register(Review)
admin.site.register(Watchlist)