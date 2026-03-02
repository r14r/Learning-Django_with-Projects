from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from grade_tracker.models import Course, Grade

COURSES = [
    {
        'name': 'Introduction to Python',
        'code': 'CS101',
        'description': 'Fundamentals of Python programming.',
        'grades': [
            {'assignment': 'Quiz 1', 'score': 90, 'max_score': 100},
            {'assignment': 'Midterm', 'score': 82, 'max_score': 100},
            {'assignment': 'Final Project', 'score': 95, 'max_score': 100},
        ],
    },
    {
        'name': 'Web Development with Django',
        'code': 'CS201',
        'description': 'Building web applications with Django.',
        'grades': [
            {'assignment': 'Assignment 1', 'score': 88, 'max_score': 100},
            {'assignment': 'Project Milestone', 'score': 91, 'max_score': 100},
            {'assignment': 'Final Exam', 'score': 87, 'max_score': 100},
        ],
    },
]


class Command(BaseCommand):
    help = 'Seed the database with sample courses and grades'

    def handle(self, *args, **options):
        user, _ = User.objects.get_or_create(
            username='admin',
            defaults={'is_staff': True, 'is_superuser': True},
        )
        if not user.has_usable_password():
            user.set_password('admin')
            user.save()

        for data in COURSES:
            course, created = Course.objects.get_or_create(
                name=data['name'],
                student=user,
                defaults={'code': data['code'], 'description': data['description']},
            )
            if created:
                for g in data['grades']:
                    Grade.objects.create(course=course, **g)

        self.stdout.write(self.style.SUCCESS(f'Seeded {len(COURSES)} courses with grades.'))
