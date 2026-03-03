# Tips & Implementation Guide: Movie Database

## 1. Annotate Average Rating

```python
from django.db.models import Avg

movies = Movie.objects.annotate(avg_rating=Avg('rating__score'))
```

## 2. Upsert Rating

```python
@login_required
def rate_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    score = int(request.POST.get('score', 0))
    if 1 <= score <= 10:
        Rating.objects.update_or_create(
            movie=movie, user=request.user,
            defaults={'score': score}
        )
    return redirect(movie.get_absolute_url())
```

## 3. Watchlist Toggle

```python
class Watchlist(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    class Meta: unique_together = ('user', 'movie')
```
