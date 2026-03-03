# Tips & Implementation Guide: Hotel Booking

## 1. Availability Check

```python
def is_room_available(room, check_in, check_out):
    overlapping = Booking.objects.filter(
        room=room,
        status__in=['pending', 'confirmed'],
    ).exclude(
        check_out__lte=check_in
    ).exclude(
        check_in__gte=check_out
    )
    return not overlapping.exists()
```

## 2. Total Price Calculation

```python
from decimal import Decimal

def calculate_total(room, check_in, check_out):
    nights = (check_out - check_in).days
    return Decimal(nights) * room.price_night
```

## 3. Booking Form Validation

```python
class BookingForm(forms.ModelForm):
    def clean(self):
        cd = super().clean()
        if cd.get('check_in') and cd.get('check_out'):
            if cd['check_out'] <= cd['check_in']:
                raise ValidationError('Check-out must be after check-in.')
        return cd
```
