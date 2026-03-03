# Tips & Implementation Guide: Newsletter System

## 1. Token-Based Subscription

```python
import uuid
class Subscriber(models.Model):
    email     = models.EmailField(unique=True)
    token     = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    confirmed = models.BooleanField(default=False)
```

## 2. Confirmation Email

```python
from django.core.mail import send_mail
from django.urls import reverse

def subscribe_view(request):
    if form.is_valid():
        subscriber, created = Subscriber.objects.get_or_create(
            email=form.cleaned_data['email']
        )
        confirm_url = request.build_absolute_uri(
            reverse('newsletter_system:confirm', kwargs={'token': subscriber.token})
        )
        send_mail(
            'Confirm your subscription',
            f'Click to confirm: {confirm_url}',
            'noreply@example.com',
            [subscriber.email],
        )
```

## 3. Send Campaign

```python
from django.core.mail import send_mass_mail

def send_campaign(request, pk):
    campaign     = get_object_or_404(Campaign, pk=pk, sent_at__isnull=True)
    subscribers  = Subscriber.objects.filter(confirmed=True)
    messages_out = [
        (campaign.subject, campaign.body_text, 'noreply@example.com', [s.email])
        for s in subscribers
    ]
    send_mass_mail(messages_out)
    campaign.sent_at = timezone.now()
    campaign.save()
```
