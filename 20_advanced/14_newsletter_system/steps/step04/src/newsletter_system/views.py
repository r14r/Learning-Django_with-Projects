from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, send_mass_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse_lazy
from .models import Subscriber, Campaign
from .forms import SubscribeForm, CampaignForm


def subscribe_view(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            sub, created = Subscriber.objects.get_or_create(
                email=form.cleaned_data['email'],
                defaults={'name': form.cleaned_data.get('name', '')}
            )
            confirm_url = request.build_absolute_uri(sub.get_confirm_url())
            send_mail(
                'Confirm your newsletter subscription',
                f'Click to confirm: {confirm_url}',
                'noreply@example.com',
                [sub.email],
            )
            return render(request, 'newsletter_system/subscribed.html', {})
    else:
        form = SubscribeForm()
    return render(request, 'newsletter_system/subscribe.html', {'form': form})


def confirm_view(request, token):
    sub = get_object_or_404(Subscriber, token=token)
    sub.confirmed = True
    sub.save()
    return render(request, 'newsletter_system/confirmed.html', {'subscriber': sub})


def unsubscribe_view(request, token):
    sub = get_object_or_404(Subscriber, token=token)
    sub.confirmed = False
    sub.save()
    return render(request, 'newsletter_system/unsubscribed.html', {})


class CampaignListView(LoginRequiredMixin, ListView):
    model               = Campaign
    template_name       = 'newsletter_system/campaign_list.html'
    context_object_name = 'campaigns'

    def get_queryset(self):
        return Campaign.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['subscriber_count'] = Subscriber.objects.filter(confirmed=True).count()
        return ctx


class CampaignCreateView(LoginRequiredMixin, CreateView):
    model         = Campaign
    form_class    = CampaignForm
    template_name = 'newsletter_system/campaign_form.html'
    success_url   = reverse_lazy('newsletter_system:campaign-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


@login_required
def send_campaign(request, pk):
    campaign    = get_object_or_404(Campaign, pk=pk, owner=request.user, sent_at__isnull=True)
    subscribers = Subscriber.objects.filter(confirmed=True)
    messages    = [
        (campaign.subject, campaign.body_text, 'noreply@example.com', [s.email])
        for s in subscribers
    ]
    send_mass_mail(messages, fail_silently=True)
    campaign.sent_at = timezone.now()
    campaign.save()
    return redirect('newsletter_system:campaign-list')