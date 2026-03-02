from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Project
from .forms import ProjectForm


class ProjectListView(ListView):
    model = Project
    template_name = 'personal_portfolio/item_list.html'
    context_object_name = 'object_list'
    paginate_by = 9


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'personal_portfolio/item_detail.html'


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model      = Project
    form_class = ProjectForm
    template_name = 'personal_portfolio/item_form.html'
    success_url = reverse_lazy('personal_portfolio:list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model      = Project
    form_class = ProjectForm
    template_name = 'personal_portfolio/item_form.html'
    success_url = reverse_lazy('personal_portfolio:list')


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model       = Project
    template_name = 'personal_portfolio/item_confirm_delete.html'
    success_url = reverse_lazy('personal_portfolio:list')
