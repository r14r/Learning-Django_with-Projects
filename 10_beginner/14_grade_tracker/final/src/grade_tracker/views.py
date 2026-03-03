from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView

from .forms import CourseForm, GradeForm
from .models import Course, Grade


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'grade_tracker/item_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return Course.objects.filter(student=self.request.user)


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'grade_tracker/item_detail.html'


class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'grade_tracker/item_form.html'
    success_url = reverse_lazy('grade_tracker:list')

    def form_valid(self, form):
        form.instance.student = self.request.user
        return super().form_valid(form)


class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = 'grade_tracker/item_confirm_delete.html'
    success_url = reverse_lazy('grade_tracker:list')


class GradeCreateView(LoginRequiredMixin, CreateView):
    model = Grade
    form_class = GradeForm
    template_name = 'grade_tracker/item_form.html'

    def get_course(self):
        return get_object_or_404(Course, pk=self.kwargs['course_pk'], student=self.request.user)

    def form_valid(self, form):
        form.instance.course = self.get_course()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('grade_tracker:detail', kwargs={'pk': self.kwargs['course_pk']})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['course'] = self.get_course()
        return ctx


class GradeDeleteView(LoginRequiredMixin, DeleteView):
    model = Grade
    template_name = 'grade_tracker/item_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('grade_tracker:detail', kwargs={'pk': self.object.course.pk})
