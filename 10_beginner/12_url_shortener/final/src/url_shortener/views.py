from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, ListView, TemplateView

from .forms import URLShortenForm
from .models import ShortURL


class ShortenView(View):
    template_name = 'url_shortener/item_list.html'

    def get(self, request):
        from django.shortcuts import render
        form = URLShortenForm()
        recent = ShortURL.objects.all()[:10]
        return render(request, self.template_name, {'form': form, 'recent': recent})

    def post(self, request):
        from django.shortcuts import render
        form = URLShortenForm(request.POST)
        recent = ShortURL.objects.all()[:10]
        short_url = None
        if form.is_valid():
            obj = form.save(commit=False)
            if request.user.is_authenticated:
                obj.created_by = request.user
            obj.save()
            short_url = obj
        return render(request, self.template_name, {'form': form, 'recent': recent, 'short_url': short_url})


class URLListView(LoginRequiredMixin, ListView):
    model = ShortURL
    template_name = 'url_shortener/item_detail.html'
    context_object_name = 'urls'

    def get_queryset(self):
        return ShortURL.objects.filter(created_by=self.request.user)


class RedirectView(View):
    def get(self, request, short_code):
        obj = get_object_or_404(ShortURL, short_code=short_code)
        obj.clicks += 1
        obj.save()
        return redirect(obj.original_url)


class URLDeleteView(LoginRequiredMixin, DeleteView):
    model = ShortURL
    template_name = 'url_shortener/item_confirm_delete.html'
    success_url = reverse_lazy('url_shortener:my-urls')
