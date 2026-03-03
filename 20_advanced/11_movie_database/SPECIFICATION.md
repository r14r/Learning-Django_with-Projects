# Specification: Movie Database

**Level:** Advanced  
**Project:** 11_movie_database  
**Description:** IMDb-style database with ratings and reviews

---

## 1. Overview

Build an IMDb-inspired movie database where users can browse movies, actors,
and genres, submit ratings (1–10), and write reviews.

## 2. Goals

- Model movies with many actors (many-to-many), genres, and a director
- Compute average ratings efficiently
- Build search, filter (genre, year range, rating threshold) views
- Implement a watchlist feature for logged-in users

## 3. Functional Requirements

| # | Feature | Priority |
|---|---------|----------|
| 1 | Browse movies (list, search, filter) | Must |
| 2 | Movie detail with cast, genres, description | Must |
| 3 | Rate a movie 1–10 (one rating per user) | Must |
| 4 | Write and read reviews | Must |
| 5 | Actor profile page | Should |
| 6 | Genre filter page | Should |
| 7 | Watchlist (add / remove) | Should |
| 8 | Top-rated movies leaderboard | Could |

## 4. Data Model

```
Genre
├── id   : AutoField
├── name : CharField(unique=True)
└── slug : SlugField(unique=True)

Person
├── id         : AutoField
├── name       : CharField
├── birth_date : DateField(null=True)
├── bio        : TextField
└── photo      : ImageField

Movie
├── id          : AutoField
├── title       : CharField
├── slug        : SlugField(unique=True)
├── year        : IntegerField
├── duration    : PositiveIntegerField (minutes)
├── synopsis    : TextField
├── poster      : ImageField
├── director    : ForeignKey(Person, related_name='directed')
├── cast        : ManyToManyField(Person, related_name='movies')
├── genres      : ManyToManyField(Genre)
└── created_at  : DateTimeField(auto_now_add=True)

Rating
├── id     : AutoField
├── movie  : ForeignKey(Movie)
├── user   : ForeignKey(User)
├── score  : PositiveSmallIntegerField (1–10)
└── created_at : DateTimeField(auto_now_add=True)

Review
├── id         : AutoField
├── movie      : ForeignKey(Movie, related_name='reviews')
├── author     : ForeignKey(User)
├── body       : TextField
└── created_at : DateTimeField(auto_now_add=True)
```

## 5. Acceptance Criteria

- [ ] Average rating calculated from all user ratings
- [ ] One rating per user per movie (upsert)
- [ ] Watchlist add/remove toggles work
- [ ] Filter by genre and year range works
- [ ] At least 10 tests pass
