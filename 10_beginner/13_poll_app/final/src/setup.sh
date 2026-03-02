#!/bin/bash
# 1. Create a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install Django
pip install django python-decouple
pip freeze > requirements.txt

# 3. Create the project
django-admin startproject config .

# 4. Create the application
python manage.py startapp poll_app
