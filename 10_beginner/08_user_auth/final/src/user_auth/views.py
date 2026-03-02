from django.views import View
from django.views.generic import TemplateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import UserProfile
from .forms import RegisterForm, ProfileForm


class RegisterView(View):
    template_name = 'user_auth/item_confirm_delete.html'

    def get(self, request):
        return render(request, self.template_name, {'form': RegisterForm()})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_auth:list')
        return render(request, self.template_name, {'form': form})


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'user_auth/item_list.html'


class ProfileView(LoginRequiredMixin, DetailView):
    model         = UserProfile
    template_name = 'user_auth/item_detail.html'
    context_object_name = 'profile'


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model         = UserProfile
    form_class    = ProfileForm
    template_name = 'user_auth/item_form.html'
    success_url   = reverse_lazy('user_auth:list')

    def get_object(self):
        return self.request.user.profile
