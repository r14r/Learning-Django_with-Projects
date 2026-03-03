from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from .models import Genre, Movie


class MovieListView(ListView):
    template_name       = 'movie_database/movie_list.html'
    context_object_name = 'movies'
    paginate_by         = 20

    def get_queryset(self):
        qs   = Movie.objects.annotate(avg_rating=Avg('ratings__score'))
        slug = self.kwargs.get('slug')
        if slug:
            genre = get_object_or_404(Genre, slug=slug)
            qs    = qs.filter(genres=genre)
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(title__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['genres'] = Genre.objects.all()
        return ctx


class MovieDetailView(DetailView):
    model         = Movie
    slug_field    = 'slug'
    template_name = 'movie_database/movie_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['avg_rating'] = self.object.ratings.aggregate(avg=Avg('score'))['avg']
        ctx['reviews']    = self.object.reviews.select_related('author')
        return ctx