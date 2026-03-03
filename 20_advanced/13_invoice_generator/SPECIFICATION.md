# Specification: Invoice Generator

**Level:** Advanced  
**Project:** 13_invoice_generator  
**Description:** Create, manage and export PDF invoices

---

## 1. Overview

Build an invoicing application where freelancers can manage clients,
create itemised invoices, track payment status, and export invoices as PDF.

## 2. Goals

- Model clients and invoices with line items
- Auto-calculate totals (subtotal + tax)
- Generate PDF using `WeasyPrint` or `reportlab`
- Track invoice status (draft → sent → paid)

## 3. Functional Requirements

| # | Feature | Priority |
|---|---------|----------|
| 1 | Manage clients (CRUD) | Must |
| 2 | Create invoices with line items | Must |
| 3 | Auto-calculate subtotal, tax, total | Must |
| 4 | Status workflow: draft → sent → paid | Must |
| 5 | Download invoice as PDF | Must |
| 6 | Dashboard: unpaid / overdue invoices | Should |
| 7 | Email invoice to client | Could |

## 4. Data Model

```
Client
├── id           : AutoField
├── owner        : ForeignKey(User)
├── name         : CharField
├── email        : EmailField
├── address      : TextField
└── tax_id       : CharField(blank=True)

Invoice
├── id           : AutoField
├── owner        : ForeignKey(User)
├── client       : ForeignKey(Client)
├── number       : CharField(unique=True)
├── issue_date   : DateField
├── due_date     : DateField
├── status       : CharField choices=[draft, sent, paid]
├── tax_rate     : DecimalField (percentage, e.g. 0.20)
└── notes        : TextField

LineItem
├── id          : AutoField
├── invoice     : ForeignKey(Invoice, related_name='items')
├── description : CharField
├── quantity    : DecimalField
├── unit_price  : DecimalField
└── order       : PositiveIntegerField
```

## 5. Acceptance Criteria

- [ ] Line item total = quantity × unit_price
- [ ] Invoice total = subtotal × (1 + tax_rate)
- [ ] PDF exported with all items, totals and client info
- [ ] Only draft invoices can be edited/deleted
- [ ] At least 10 tests pass
