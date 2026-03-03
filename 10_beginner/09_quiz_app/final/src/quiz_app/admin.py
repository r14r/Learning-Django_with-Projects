from django.contrib import admin
from .models import Quiz, Question, Choice, QuizResult


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display  = ('title', 'author', 'created_at')
    search_fields = ('title',)
    inlines       = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'order')
    inlines      = [ChoiceInline]


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'user', 'score', 'total', 'taken_at')
