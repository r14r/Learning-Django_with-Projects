from django.contrib import admin

from .models import Course, Grade


class GradeInline(admin.TabularInline):
    model = Grade
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'student', 'created_at')
    list_filter = ('student',)
    search_fields = ('name', 'code')
    inlines = [GradeInline]


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'course', 'score', 'max_score', 'graded_on')
    list_filter = ('course',)
