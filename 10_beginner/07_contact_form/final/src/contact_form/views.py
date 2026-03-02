from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from .models import ContactMessage
from .forms import ContactForm


class ContactFormView(View):
    template_name = 'contact_form/item_list.html'

    def get(self, request):
        return render(request, self.template_name, {'form': ContactForm()})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_form:success')
        return render(request, self.template_name, {'form': form})


class ContactSuccessView(TemplateView):
    template_name = 'contact_form/item_form.html'


class MessageListView(LoginRequiredMixin, ListView):
    model               = ContactMessage
    template_name       = 'contact_form/item_confirm_delete.html'
    context_object_name = 'messages_list'
    paginate_by         = 20


class MessageDetailView(LoginRequiredMixin, DetailView):
    model         = ContactMessage
    template_name = 'contact_form/item_detail.html'

    def get_object(self):
        obj = super().get_object()
        if not obj.is_read:
            obj.is_read = True
            obj.save(update_fields=['is_read'])
        return obj


class MarkReadView(LoginRequiredMixin, View):
    def post(self, request, pk):
        msg = get_object_or_404(ContactMessage, pk=pk)
        msg.is_read = not msg.is_read
        msg.save(update_fields=['is_read'])
        return redirect('contact_form:detail', pk=pk)
