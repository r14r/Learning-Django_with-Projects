from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from .models import Quiz, QuizResult
from .forms import QuizForm


class QuizListView(ListView):
    model               = Quiz
    template_name       = 'quiz_app/item_list.html'
    context_object_name = 'quizzes'


class QuizDetailView(DetailView):
    model               = Quiz
    template_name       = 'quiz_app/item_detail.html'
    context_object_name = 'quiz'


class TakeQuizView(LoginRequiredMixin, View):
    template_name = 'quiz_app/item_list.html'

    def get(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        return render(request, 'quiz_app/take_quiz.html', {'quiz': quiz})

    def post(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        score = 0
        total = quiz.questions.count()
        for question in quiz.questions.all():
            selected = request.POST.get(f'question_{question.pk}')
            if selected:
                correct = question.choices.filter(is_correct=True).first()
                if correct and str(correct.pk) == selected:
                    score += 1
        result = QuizResult.objects.create(
            quiz=quiz, user=request.user, score=score, total=total
        )
        return redirect(reverse('quiz_app:result', kwargs={'pk': result.pk}))


class QuizResultView(LoginRequiredMixin, DetailView):
    model               = QuizResult
    template_name       = 'quiz_app/item_detail.html'
    context_object_name = 'result'


class QuizCreateView(LoginRequiredMixin, CreateView):
    model       = Quiz
    form_class  = QuizForm
    template_name = 'quiz_app/item_form.html'
    success_url = reverse_lazy('quiz_app:list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class QuizDeleteView(LoginRequiredMixin, DeleteView):
    model       = Quiz
    template_name = 'quiz_app/item_confirm_delete.html'
    success_url = reverse_lazy('quiz_app:list')
