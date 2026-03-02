from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from quiz_app.models import Quiz, Question, Choice


class Command(BaseCommand):
    help = 'Seed the database with a sample quiz'

    def handle(self, *args, **kwargs):
        author, _ = User.objects.get_or_create(
            username='quizmaster',
            defaults={'email': 'qm@example.com'},
        )
        if not author.has_usable_password():
            author.set_password('quizmaster123!')
            author.save()

        quiz, created = Quiz.objects.get_or_create(
            title='Python Basics',
            defaults={'description': 'Test your Python knowledge!', 'author': author},
        )
        if not created:
            self.stdout.write('Quiz already exists, skipping seed.')
            return

        questions_data = [
            {
                'text': 'What is the output of print(type([]))?',
                'order': 1,
                'choices': [
                    ("<class 'list'>", True),
                    ("<class 'tuple'>", False),
                    ("<class 'dict'>", False),
                    ("<class 'set'>", False),
                ],
            },
            {
                'text': 'Which keyword is used to define a function in Python?',
                'order': 2,
                'choices': [
                    ('def', True),
                    ('func', False),
                    ('function', False),
                    ('lambda', False),
                ],
            },
            {
                'text': 'What does len("hello") return?',
                'order': 3,
                'choices': [
                    ('5', True),
                    ('4', False),
                    ('6', False),
                    ('None', False),
                ],
            },
        ]

        for qdata in questions_data:
            question = Question.objects.create(
                quiz=quiz, text=qdata['text'], order=qdata['order']
            )
            for text, is_correct in qdata['choices']:
                Choice.objects.create(question=question, text=text, is_correct=is_correct)

        self.stdout.write(self.style.SUCCESS(
            f'Seeded quiz "{quiz.title}" with {len(questions_data)} questions.'
        ))
