from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from simple_blog.models import Post


class Command(BaseCommand):
    help = 'Seed database with blog posts'

    def handle(self, *args, **kwargs):
        user, _ = User.objects.get_or_create(
            username='admin',
            defaults={'is_staff': True, 'is_superuser': True}
        )
        user.set_password('admin123')
        user.save()

        posts = [
            ('Getting Started with Django', 'Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel.', 'Learn how to set up your first Django project in minutes.'),
            ('Understanding Django ORM', 'The Django ORM (Object-Relational Mapper) lets you interact with your database using Python code instead of SQL. Models define the structure of your data, and the ORM translates your Python objects into database rows automatically.', "Master database queries with Django's powerful ORM."),
            ('Building REST APIs with DRF', 'Django REST Framework is a powerful toolkit for building Web APIs. It provides serializers, viewsets, and routers that make API development fast and clean. Authentication, permissions, and throttling are all built-in.', 'Create your first REST API using Django REST Framework.'),
        ]
        for title, body, excerpt in posts:
            Post.objects.get_or_create(
                title=title,
                defaults={'body': body, 'excerpt': excerpt, 'author': user}
            )

        self.stdout.write(self.style.SUCCESS('Seeding complete: 3 blog posts created'))
