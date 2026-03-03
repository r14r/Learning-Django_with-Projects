from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    author      = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz  = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text  = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Q{self.order}: {self.text[:60]}"


class Choice(models.Model):
    question   = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text       = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class QuizResult(models.Model):
    quiz     = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    score    = models.PositiveIntegerField()
    total    = models.PositiveIntegerField()
    taken_at = models.DateTimeField(auto_now_add=True)

    @property
    def percentage(self):
        return (self.score / self.total * 100) if self.total > 0 else 0

    def __str__(self):
        return f"{self.user.username} – {self.quiz.title}: {self.score}/{self.total}"
