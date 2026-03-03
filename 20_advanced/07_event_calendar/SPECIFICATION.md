# Specification: Event Calendar

**Level:** Advanced  
**Project:** 07_event_calendar  
**Description:** Calendar application with event management

---

## 1. Overview

Build an event calendar where users can create, browse, and register for events.
Events are displayed in a monthly calendar grid and on a list view.

## 2. Goals

- Model events with start/end datetime, venue, and capacity
- Build a monthly calendar view and an upcoming-events list
- Implement user registration (RSVP) for events
- Support recurring-event patterns (basic: daily/weekly/monthly)

## 3. Functional Requirements

| # | Feature | Priority |
|---|---------|----------|
| 1 | Create and manage events | Must |
| 2 | Monthly calendar grid view | Must |
| 3 | Upcoming events list view | Must |
| 4 | Event detail page | Must |
| 5 | RSVP / register for event | Must |
| 6 | Cancel registration | Should |
| 7 | Category filter | Should |
| 8 | iCal / .ics download | Could |

## 4. Data Model

```
Category
├── id   : AutoField
├── name : CharField(max_length=100, unique=True)
└── color : CharField(max_length=7)

Event
├── id          : AutoField
├── title       : CharField(max_length=200)
├── slug        : SlugField(unique=True)
├── organiser   : ForeignKey(User)
├── category    : ForeignKey(Category, null=True)
├── description : TextField
├── venue       : CharField(max_length=200)
├── start       : DateTimeField
├── end         : DateTimeField
├── capacity    : PositiveIntegerField (0 = unlimited)
├── image       : ImageField(upload_to='events/', blank=True)
└── is_public   : BooleanField(default=True)

Registration
├── id         : AutoField
├── event      : ForeignKey(Event, related_name='registrations')
├── attendee   : ForeignKey(User)
└── created_at : DateTimeField(auto_now_add=True)
```

## 5. URL Structure

| URL | View | Name |
|-----|------|------|
| `/` | UpcomingEventsView | `event_calendar:list` |
| `/calendar/<year>/<month>/` | CalendarView | `event_calendar:calendar` |
| `/event/<slug>/` | EventDetailView | `event_calendar:detail` |
| `/event/create/` | EventCreateView | `event_calendar:create` |
| `/event/<slug>/register/` | register_view | `event_calendar:register` |
| `/event/<slug>/cancel/` | cancel_view | `event_calendar:cancel` |
| `/my-events/` | MyEventsView | `event_calendar:my-events` |

## 6. Acceptance Criteria

- [ ] Monthly calendar shows events on correct days
- [ ] RSVP respected capacity limits
- [ ] User can see their registered events on My Events page
- [ ] At least 10 tests pass
