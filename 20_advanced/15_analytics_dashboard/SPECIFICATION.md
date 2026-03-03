# Specification: Analytics Dashboard

**Level:** Advanced  
**Project:** 15_analytics_dashboard  
**Description:** Data visualisation dashboard with charts

---

## 1. Overview

Build a website analytics dashboard that tracks page views and custom events,
then visualises the data with interactive charts (using Chart.js).

## 2. Goals

- Record page views automatically via a Django middleware or JS beacon
- Store custom events (button clicks, form submissions) via an API endpoint
- Build a dashboard with line charts (daily views), bar charts (top pages),
  and summary cards (total views, unique visitors, bounce rate)

## 3. Functional Requirements

| # | Feature | Priority |
|---|---------|----------|
| 1 | Auto-track page views (middleware) | Must |
| 2 | API endpoint to record custom events | Must |
| 3 | Dashboard: total visits today / this week / this month | Must |
| 4 | Chart: daily page views (last 30 days) | Must |
| 5 | Top 10 most-visited pages | Must |
| 6 | Browser / OS breakdown | Should |
| 7 | Real-time visitors (last 5 min) | Could |

## 4. Data Model

```
PageView
├── id         : AutoField
├── path       : CharField(max_length=500)
├── method     : CharField(max_length=10)
├── user       : ForeignKey(User, null=True)
├── session_key : CharField(max_length=40)
├── user_agent : TextField(blank=True)
├── referer    : URLField(blank=True)
├── ip_address : GenericIPAddressField(null=True)
└── timestamp  : DateTimeField(auto_now_add=True)

Event
├── id         : AutoField
├── name       : CharField(max_length=100)
├── properties : JSONField(default=dict)
├── session_key : CharField(max_length=40, blank=True)
└── timestamp  : DateTimeField(auto_now_add=True)
```

## 5. URL Structure

| URL | View | Name |
|-----|------|------|
| `/dashboard/` | DashboardView | `analytics_dashboard:dashboard` |
| `/api/event/` | record_event | `analytics_dashboard:event` |
| `/api/stats/daily/` | daily_stats | `analytics_dashboard:daily-stats` |

## 6. Acceptance Criteria

- [ ] Middleware records page views for every non-admin request
- [ ] Dashboard shows correct counts for today
- [ ] Top pages ordered by view count
- [ ] At least 8 tests pass
