# Specification: Newsletter System

**Level:** Advanced  
**Project:** 14_newsletter_system  
**Description:** Email subscription and campaign management

---

## 1. Overview

Build a newsletter platform where visitors can subscribe, admins can compose
and send email campaigns, and subscribers can unsubscribe via a tokenised link.

## 2. Goals

- Manage mailing list with double opt-in confirmation
- Compose HTML campaigns and preview them
- Send campaigns via Django's email backend (configurable SMTP)
- Track open/click stats (optional)

## 3. Functional Requirements

| # | Feature | Priority |
|---|---------|----------|
| 1 | Subscribe via public form | Must |
| 2 | Confirmation email with activation link | Must |
| 3 | Unsubscribe via token link | Must |
| 4 | Create and manage campaigns | Must |
| 5 | Send campaign to all confirmed subscribers | Must |
| 6 | Subscriber count dashboard | Should |
| 7 | Campaign open tracking (image pixel) | Could |

## 4. Data Model

```
Subscriber
├── id         : AutoField
├── email      : EmailField(unique=True)
├── name       : CharField(max_length=100, blank=True)
├── token      : UUIDField(default=uuid4, unique=True)
├── confirmed  : BooleanField(default=False)
└── created_at : DateTimeField(auto_now_add=True)

Campaign
├── id           : AutoField
├── owner        : ForeignKey(User)
├── subject      : CharField(max_length=300)
├── body_text    : TextField
├── body_html    : TextField(blank=True)
├── sent_at      : DateTimeField(null=True, blank=True)
└── created_at   : DateTimeField(auto_now_add=True)
```

## 5. URL Structure

| URL | View | Name |
|-----|------|------|
| `/subscribe/` | subscribe_view | `newsletter_system:subscribe` |
| `/confirm/<token>/` | confirm_view | `newsletter_system:confirm` |
| `/unsubscribe/<token>/` | unsubscribe_view | `newsletter_system:unsubscribe` |
| `/campaigns/` | CampaignListView | `newsletter_system:campaign-list` |
| `/campaigns/create/` | CampaignCreateView | `newsletter_system:campaign-create` |
| `/campaigns/<pk>/send/` | send_campaign | `newsletter_system:send` |

## 6. Acceptance Criteria

- [ ] Subscribe form validates email format
- [ ] Confirmation link activates the subscriber
- [ ] Unsubscribe link removes subscriber
- [ ] Campaign sends one email per confirmed subscriber
- [ ] At least 8 tests pass
