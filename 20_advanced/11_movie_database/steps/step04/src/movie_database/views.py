from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect
from .models import Genre, Movie, Rating, Review, Watchlist, Person
from .forms import ReviewForm


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
        year = self.request.GET.get('year')
        if year:
            qs = qs.filter(year=year)
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
        ctx['form']       = ReviewForm()
        if self.request.user.is_authenticated:
            ctx['user_rating'] = Rating.objects.filter(
                movie=self.object, user=self.request.user
            ).first()
            ctx['in_watchlist'] = Watchlist.objects.filter(
                user=self.request.user, movie=self.object
            ).exists()
        return ctx


@login_required
def rate_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    score = int(request.POST.get('score', 0))
    if 1 <= score <= 10:
        Rating.objects.update_or_create(
            movie=movie, user=request.user, defaults={'score': score}
        )
    return redirect(movie.get_absolute_url())


@login_required
def add_review(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            r        = form.save(commit=False)
            r.movie  = movie
            r.author = request.user
            r.save()
    return redirect(movie.get_absolute_url())


@login_required
def watchlist_toggle(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    wl, created = Watchlist.objects.get_or_create(user=request.user, movie=movie)
    if not created:
        wl.delete()
    return redirect(movie.get_absolute_url())