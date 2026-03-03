# Specification: Hotel Booking System

**Level:** Advanced  
**Project:** 12_hotel_booking  
**Description:** Room availability check and reservation system

---

## 1. Overview

Build a hotel booking system where administrators manage rooms and guests can
search availability, make reservations, and view their booking history.

## 2. Goals

- Model rooms with type (single, double, suite), capacity and price per night
- Check availability (no overlapping confirmed bookings)
- Calculate total cost based on check-in / check-out dates
- Send booking confirmation (simulated via console email backend)

## 3. Functional Requirements

| # | Feature | Priority |
|---|---------|----------|
| 1 | List available rooms for a date range | Must |
| 2 | Room detail page with photos and amenities | Must |
| 3 | Book a room (requires login) | Must |
| 4 | Booking confirmation page | Must |
| 5 | Guest dashboard: view / cancel bookings | Must |
| 6 | Admin: manage rooms and all bookings | Should |
| 7 | Reviews for completed stays | Could |

## 4. Data Model

```
RoomType: single | double | suite | deluxe

Room
├── id          : AutoField
├── number      : CharField(max_length=10, unique=True)
├── room_type   : CharField(choices=RoomType)
├── capacity    : PositiveIntegerField
├── price_night : DecimalField
├── description : TextField
├── amenities   : TextField (comma-separated)
├── image       : ImageField
└── available   : BooleanField(default=True)

Booking
├── id          : AutoField
├── room        : ForeignKey(Room)
├── guest       : ForeignKey(User)
├── check_in    : DateField
├── check_out   : DateField
├── guests      : PositiveIntegerField
├── total_price : DecimalField
├── status      : CharField choices=[pending, confirmed, cancelled]
└── created_at  : DateTimeField(auto_now_add=True)
```

## 5. URL Structure

| URL | View | Name |
|-----|------|------|
| `/` | RoomListView | `hotel_booking:list` |
| `/room/<pk>/` | RoomDetailView | `hotel_booking:room-detail` |
| `/book/<pk>/` | book_view | `hotel_booking:book` |
| `/bookings/` | GuestDashboard | `hotel_booking:my-bookings` |
| `/bookings/<pk>/cancel/` | cancel_booking | `hotel_booking:cancel` |

## 6. Acceptance Criteria

- [ ] Availability check prevents double-booking
- [ ] Total price computed: nights × price_per_night
- [ ] Guest can cancel pending/confirmed bookings
- [ ] At least 10 tests pass
