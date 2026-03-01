# Specification: Full-Stack with React

**Level:** Expert  
**Project:** 11_fullstack_react  
**Description:** Django backend + React SPA with DRF and Vite

---

## 1. Overview

Django backend + React SPA with DRF and Vite. This project teaches fundamental Django concepts appropriate for the **expert** level including models, views, templates, forms and URL routing.

## 2. Goals

- Understand the Django request/response cycle
- Create and apply database models with Django ORM
- Build HTML templates using the Django template language
- Handle user input through Django forms
- Write clean, testable Django code

## 3. Functional Requirements

### 3.1 Core Features

| # | Feature | Priority |
|---|---------|----------|
| 1 | Display a home page | Must |
| 2 | List and detail views for the main entity | Must |
| 3 | Create / Edit / Delete (CRUD) operations | Must |
| 4 | Basic user authentication (login/logout) | Should |
| 5 | Input validation and error messages | Should |
| 6 | Responsive HTML layout | Could |

### 3.2 User Stories

- **As a visitor**, I want to browse the main content so that I can find what I need.
- **As a registered user**, I want to create and manage my own entries.
- **As an admin**, I want to manage all content through the Django admin interface.

## 4. Non-Functional Requirements

- The application must run on Django 4.2+ with Python 3.11+
- Pages must load within 2 seconds on a local development server
- All forms must validate input and display meaningful error messages
- Code must follow PEP 8 style guidelines

## 5. Data Model

```
Entity
├── id          : AutoField (primary key)
├── title       : CharField(max_length=200)
├── description : TextField(blank=True)
├── created_at  : DateTimeField(auto_now_add=True)
├── updated_at  : DateTimeField(auto_now=True)
└── author      : ForeignKey(User, on_delete=CASCADE)
```

## 6. URL Structure

| URL Pattern | View | Name |
|-------------|------|------|
| `/` | HomeView | `home` |
| `/items/` | ListView | `item-list` |
| `/items/<pk>/` | DetailView | `item-detail` |
| `/items/create/` | CreateView | `item-create` |
| `/items/<pk>/edit/` | UpdateView | `item-update` |
| `/items/<pk>/delete/` | DeleteView | `item-delete` |

## 7. Pages and Templates

- **Home** – Landing page with a brief introduction and call-to-action.
- **List** – Paginated list of all items with search/filter.
- **Detail** – Full view of a single item.
- **Form** – Shared create/edit form with client-side validation.
- **Delete confirmation** – Confirmation page before deleting.

## 8. Acceptance Criteria

- [ ] All CRUD operations work correctly
- [ ] Forms display validation errors inline
- [ ] Django admin shows all models with search and filter
- [ ] At least 10 unit/integration tests pass (`python manage.py test`)
- [ ] No secrets are hard-coded; environment variables are used
- [ ] `requirements.txt` lists all dependencies with pinned versions

## 9. Out of Scope

- Payment processing
- Real-time features (WebSockets)
- Third-party social authentication
