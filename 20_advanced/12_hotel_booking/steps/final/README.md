# Final – Complete Running Application

## What this is
This is the **complete, fully-integrated application** for **Hotel Booking**.
It combines all code from steps 01 through 05 into a single working project that
you can run immediately.

## Quick start

```bash
# 1. Copy (or use) this src/ directory as your working directory
cd src

# 2. Set up a virtual environment and install dependencies
just setup        # requires https://just.systems

# – or, without just –
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Create a .env file from the example
cp .env.example .env   # then edit .env and set SECRET_KEY

# 4. Apply migrations
python manage.py migrate          # or: just migrate

# 5. (Optional) Create an admin superuser
python manage.py createsuperuser  # or: just createsuperuser

# 6. Run the development server
python manage.py runserver        # or: just run
```

Open **http://127.0.0.1:8000/** in your browser.

## Available `just` commands

| Command | Description |
|---------|-------------|
| `just setup` | Create `.venv` and install all dependencies |
| `just install` | Install dependencies (assumes `.venv` exists) |
| `just migrate` | Apply database migrations |
| `just makemigrations` | Generate new migration files |
| `just run` | Start the development server |
| `just test` | Run the test suite |
| `just shell` | Open the Django interactive shell |
| `just createsuperuser` | Create an admin superuser |
| `just collectstatic` | Collect static files |
| `just check` | Run Django system checks |

## Files included

  - `.env.example`
  - `config/settings.py`
  - `config/urls.py`
  - `hotel_booking/admin.py`
  - `hotel_booking/forms.py`
  - `hotel_booking/models.py`
  - `hotel_booking/tests.py`
  - `hotel_booking/urls.py`
  - `hotel_booking/views.py`
  - `registration/login.html`
  - `requirements.txt`
  - `setup.sh`
  - `templates/base.html`
  - `justfile`

## How this was built

This final step merges the incremental changes from all five learning steps:

| Step | Focus |
|------|-------|
| step01 | Project setup, settings, first view |
| step02 | Models and Django admin |
| step03 | Templates, URL routing, class-based views |
| step04 | Forms, CRUD operations |
| step05 | Authentication, tests, deployment prep |

Refer to each individual step's `README.md` for the explanations of what was
added at each stage.
