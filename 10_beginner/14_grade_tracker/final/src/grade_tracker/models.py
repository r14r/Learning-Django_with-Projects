from django.contrib.auth.models import User
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def average_grade(self):
        grades = self.grades.all()
        if not grades:
            return None
        total = sum(g.percentage for g in grades)
        return round(total / len(grades), 2)


class Grade(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grades')
    assignment = models.CharField(max_length=200)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    graded_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.assignment}: {self.score}/{self.max_score}"

    @property
    def percentage(self):
        if self.max_score > 0:
            return float(self.score) / float(self.max_score) * 100
        return 0
