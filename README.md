# Learning Django with Projects

A comprehensive collection of **45 Django projects** organised by difficulty level, designed to help you learn Django through practical, hands-on experience. Each project comes with a detailed specification, implementation tips and five incremental steps of working source code.

## 📚 Project Structure

This repository contains 45 projects divided into three difficulty levels:

- **Beginner** (15 projects): Django fundamentals — models, views, templates, forms, admin
- **Advanced** (15 projects): Real-world features — REST APIs, authentication, file uploads, WebSockets
- **Expert** (15 projects): Production-grade patterns — multi-tenancy, Celery, GraphQL, Docker, CI/CD

Each project folder contains:

| File / Folder | Description |
|---|---|
| `SPECIFICATION.md` | Detailed specification: goals, user stories, data model, URL structure, acceptance criteria |
| `TIPS.md` | Implementation guide: architecture, recommended libraries, models, views, forms, deployment tips |
| `steps/step01/` … `steps/step05/` | Working source code from initial scaffold to fully featured application |

---

## 🟢 Beginner Level

Perfect for developers new to Django. Learn the MTV pattern, ORM basics, forms and the built-in admin.

| # | Project | Description |
|---|---------|-------------|
| 01 | [Hello Django](beginner/01_hello_django) | Your first Django "Hello World" web application |
| 02 | [Personal Portfolio](beginner/02_personal_portfolio) | A static portfolio website with templates |
| 03 | [Todo List](beginner/03_todo_list) | Basic CRUD todo application with models and views |
| 04 | [Simple Blog](beginner/04_simple_blog) | Blog with posts, list view and detail view |
| 05 | [Web Calculator](beginner/05_web_calculator) | Browser-based arithmetic calculator |
| 06 | [Temperature Converter](beginner/06_temperature_converter) | Unit conversion app (°C, °F, Kelvin) |
| 07 | [Contact Form](beginner/07_contact_form) | Form handling, validation and email sending |
| 08 | [User Authentication](beginner/08_user_auth) | Registration, login, logout and profile |
| 09 | [Quiz App](beginner/09_quiz_app) | Multiple-choice quiz with score tracking |
| 10 | [Book Library](beginner/10_book_library) | Book catalog with search and CRUD operations |
| 11 | [Notes App](beginner/11_notes_app) | Create, read, update and delete personal notes |
| 12 | [URL Shortener](beginner/12_url_shortener) | Shorten long URLs and track click counts |
| 13 | [Poll App](beginner/13_poll_app) | Create polls and vote on them |
| 14 | [Grade Tracker](beginner/14_grade_tracker) | Track student grades and compute averages |
| 15 | [Weather Display](beginner/15_weather_display) | Display weather info fetched from an external API |

---

## 🔵 Advanced Level

Build on the fundamentals with real-world libraries and production-ready patterns.

| # | Project | Description |
|---|---------|-------------|
| 01 | [REST API with DRF](advanced/01_rest_api) | Full REST API using Django REST Framework |
| 02 | [E-Commerce Store](advanced/02_ecommerce_store) | Product catalog, shopping cart and checkout |
| 03 | [Blog with Comments](advanced/03_blog_with_comments) | Blog with user comments, pagination and tags |
| 04 | [Real-Time Chat](advanced/04_chat_app) | WebSocket-based chat using Django Channels |
| 05 | [Advanced Task Manager](advanced/05_task_manager) | Task manager with priorities, deadlines and filters |
| 06 | [Recipe Book](advanced/06_recipe_book) | Recipe website with ingredients and categories |
| 07 | [Event Calendar](advanced/07_event_calendar) | Calendar application with event management |
| 08 | [File Upload Manager](advanced/08_file_manager) | Upload, organise and serve files securely |
| 09 | [Social Network](advanced/09_social_network) | User profiles, following, posts and likes |
| 10 | [Job Board](advanced/10_job_board) | Post and search job listings with applications |
| 11 | [Movie Database](advanced/11_movie_database) | IMDb-style database with ratings and reviews |
| 12 | [Hotel Booking](advanced/12_hotel_booking) | Room availability check and reservation system |
| 13 | [Invoice Generator](advanced/13_invoice_generator) | Create, manage and export PDF invoices |
| 14 | [Newsletter System](advanced/14_newsletter_system) | Email subscription and campaign management |
| 15 | [Analytics Dashboard](advanced/15_analytics_dashboard) | Data visualisation dashboard with charts |

---

## 🔴 Expert Level

Master advanced Django patterns and build production-grade, scalable applications.

| # | Project | Description |
|---|---------|-------------|
| 01 | [Full E-Commerce Platform](expert/01_ecommerce_platform) | Complete shop with Stripe payments and inventory |
| 02 | [Multi-Tenant SaaS](expert/02_saas_platform) | SaaS with per-tenant schemas using django-tenants |
| 03 | [Real-Time Notifications](expert/03_realtime_notifications) | Push notifications via WebSockets and Channels |
| 04 | [GraphQL API](expert/04_graphql_api) | GraphQL endpoint using Graphene-Django |
| 05 | [Microservices Architecture](expert/05_microservices) | Decomposed Django services communicating via REST |
| 06 | [ML Model Integration](expert/06_ml_integration) | Serve a scikit-learn / PyTorch model through Django |
| 07 | [Full-Text Search Engine](expert/07_search_engine) | Elasticsearch integration with django-elasticsearch-dsl |
| 08 | [Distributed Task Queue](expert/08_celery_tasks) | Background tasks with Celery, Redis and Flower |
| 09 | [Multi-Language CMS](expert/09_multilang_cms) | Content management with i18n and django-parler |
| 10 | [API Gateway](expert/10_api_gateway) | Rate limiting, JWT auth and request routing |
| 11 | [Full-Stack with React](expert/11_fullstack_react) | Django backend + React SPA with DRF and Vite |
| 12 | [Role-Based Access Control](expert/12_rbac_system) | Fine-grained permissions with django-guardian |
| 13 | [Social Authentication](expert/13_social_auth) | OAuth2 social login with django-allauth |
| 14 | [Docker & Kubernetes Deploy](expert/14_docker_deployment) | Containerised Django app deployed to Kubernetes |
| 15 | [Advanced Testing](expert/15_testing_framework) | Full test suite with pytest, factory_boy and coverage |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- pip / pipenv / poetry

### Quick Start (any project)

```bash
# Clone the repository
git clone https://github.com/r14r/Learning-Django_with-Projects.git
cd Learning-Django_with-Projects

# Enter any project, e.g. the beginner Todo List
cd beginner/03_todo_list

# Read the specification and tips first
cat SPECIFICATION.md
cat TIPS.md

# Start from Step 1 and work your way up
cat steps/step01/README.md
```

### Recommended Workflow

1. Read **SPECIFICATION.md** to understand what you are building.
2. Read **TIPS.md** for architecture hints, library recommendations and code snippets.
3. Implement the project yourself, step by step.
4. Compare your solution with the reference implementation in each `steps/stepNN/README.md`.

---

## 🛠️ Technology Stack

| Package | Purpose |
|---------|---------|
| Django 4.2 LTS | Web framework |
| Django REST Framework | REST APIs |
| Django Channels | WebSockets / async |
| Celery + Redis | Background tasks |
| Graphene-Django | GraphQL |
| django-allauth | Authentication |
| django-guardian | Object-level permissions |
| Elasticsearch DSL | Full-text search |
| Whitenoise | Static file serving |
| pytest-django | Testing |
| Docker / Kubernetes | Deployment |

---

## 📄 Licence

MIT — see [LICENSE](LICENSE) for details.
