from django.shortcuts import render, get_object_or_404, redirect
from .models import Subscriber
from .forms import SubscribeForm


def subscribe_view(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            Subscriber.objects.get_or_create(
                email=form.cleaned_data['email'],
                defaults={'name': form.cleaned_data.get('name', '')}
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