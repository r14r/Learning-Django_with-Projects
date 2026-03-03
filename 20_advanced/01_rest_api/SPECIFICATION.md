# Specification: REST API with Django REST Framework

**Level:** Advanced  
**Project:** 01_rest_api  
**Description:** Full REST API using Django REST Framework

---

## 1. Overview

Build a production-ready REST API for a **Book Library** service using Django REST
Framework (DRF). The API exposes books, authors, and reviews with full CRUD,
filtering, searching, pagination, and token-based authentication.

## 2. Goals

- Understand how to design and build a REST API with DRF
- Use ModelSerializer, ViewSet, and DefaultRouter
- Implement token authentication and per-object permissions
- Add filtering, search, and ordering via `django-filter`
- Write comprehensive API tests with DRF's `APITestCase`

## 3. Functional Requirements

### 3.1 Core Features

| # | Feature | Priority |
|---|---------|----------|
| 1 | CRUD endpoints for Books | Must |
| 2 | CRUD endpoints for Authors | Must |
| 3 | Nested reviews on a book | Must |
| 4 | Token-based authentication (login / register) | Must |
| 5 | Search books by title or author name | Should |
| 6 | Filter books by genre and published year | Should |
| 7 | Pagination (page-based, 20 per page) | Should |
| 8 | Browsable API (DRF default) | Could |

### 3.2 User Stories

- **As a consumer**, I want to list books with `GET /api/books/` so I can browse the catalogue.
- **As a consumer**, I want to search for books with `?search=` so I can find what I need.
- **As an authenticated user**, I want to `POST /api/books/` to add a new book.
- **As the book owner**, I want to `PUT /api/books/{id}/` to update my book.
- **As an authenticated user**, I want to `POST /api/books/{id}/reviews/` to leave a review.

## 4. Non-Functional Requirements

- All endpoints return JSON (Content-Type: application/json)
- Authentication uses `Token` header (`Authorization: Token <token>`)
- API must return proper HTTP status codes (200, 201, 400, 401, 403, 404)
- Code must follow PEP 8 and DRF conventions

## 5. Data Model

```
Author
├── id          : AutoField
├── name        : CharField(max_length=200)
├── bio         : TextField(blank=True)
└── created_at  : DateTimeField(auto_now_add=True)

Book
├── id           : AutoField
├── title        : CharField(max_length=300)
├── author       : ForeignKey(Author)
├── genre        : CharField(max_length=100)
├── published    : IntegerField (year)
├── description  : TextField(blank=True)
├── cover        : ImageField(upload_to='covers/', blank=True)
├── owner        : ForeignKey(User)  ← who added the record
└── created_at   : DateTimeField(auto_now_add=True)

Review
├── id         : AutoField
├── book       : ForeignKey(Book, related_name='reviews')
├── author     : ForeignKey(User)
├── rating     : PositiveSmallIntegerField (1–5)
├── body       : TextField
└── created_at : DateTimeField(auto_now_add=True)
```

## 6. API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| POST | `/api/auth/register/` | Register a new user |
| POST | `/api/auth/login/` | Obtain auth token |
| GET | `/api/authors/` | List authors |
| POST | `/api/authors/` | Create author (auth required) |
| GET/PUT/DELETE | `/api/authors/{id}/` | Detail / update / delete |
| GET | `/api/books/` | List books (search, filter, paginate) |
| POST | `/api/books/` | Create book (auth required) |
| GET/PUT/DELETE | `/api/books/{id}/` | Detail / update / delete |
| GET/POST | `/api/books/{id}/reviews/` | List or add reviews |

## 7. Acceptance Criteria

- [ ] All CRUD operations return correct HTTP status codes
- [ ] Unauthenticated requests to protected endpoints return 401
- [ ] Only the record owner can update or delete it (403 otherwise)
- [ ] Search and filter query parameters work correctly
- [ ] At least 12 API tests pass (`python manage.py test`)
- [ ] `requirements.txt` pins all dependencies

## 8. Out of Scope

- OAuth2 / social login
- Real-time WebSocket notifications
- Full-text search with Elasticsearch
