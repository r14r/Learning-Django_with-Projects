# Specification: E-Commerce Store

**Level:** Advanced  
**Project:** 02_ecommerce_store  
**Description:** Product catalog, shopping cart and checkout

---

## 1. Overview

Build a working e-commerce store with a product catalogue, a session-based shopping
cart, and a checkout workflow that creates `Order` records.

## 2. Goals

- Model products with categories, images and inventory
- Implement a session-based cart without requiring login to browse
- Build a checkout form that creates an Order and clears the cart
- Protect the order history with login-required views

## 3. Functional Requirements

### 3.1 Core Features

| # | Feature | Priority |
|---|---------|----------|
| 1 | Product list with category filter and search | Must |
| 2 | Product detail page with add-to-cart button | Must |
| 3 | Cart page (view, update quantity, remove) | Must |
| 4 | Checkout form (name, email, address) | Must |
| 5 | Order confirmation page | Must |
| 6 | Order history for logged-in users | Should |
| 7 | Admin: manage products, categories, orders | Should |
| 8 | Low-stock warnings | Could |

### 3.2 User Stories

- **As a shopper**, I can browse products by category and add them to my cart.
- **As a shopper**, I can update quantities or remove items from my cart.
- **As a shopper**, I can check out by entering my shipping details.
- **As a logged-in user**, I can see my past orders.
- **As an admin**, I can add, edit and remove products and see all orders.

## 4. Data Model

```
Category
├── id    : AutoField
├── name  : CharField(max_length=100)
└── slug  : SlugField(unique=True)

Product
├── id          : AutoField
├── category    : ForeignKey(Category)
├── name        : CharField(max_length=200)
├── slug        : SlugField(unique=True)
├── description : TextField
├── price       : DecimalField(max_digits=8, decimal_places=2)
├── image       : ImageField(upload_to='products/')
├── stock       : PositiveIntegerField
├── available   : BooleanField(default=True)
└── created_at  : DateTimeField(auto_now_add=True)

Order
├── id           : AutoField
├── user         : ForeignKey(User, null=True)
├── first_name   : CharField
├── last_name    : CharField
├── email        : EmailField
├── address      : TextField
├── created_at   : DateTimeField(auto_now_add=True)
├── paid         : BooleanField(default=False)
└── items        : OrderItem[]

OrderItem
├── order    : ForeignKey(Order)
├── product  : ForeignKey(Product)
├── price    : DecimalField  (snapshot at purchase time)
└── quantity : PositiveIntegerField
```

## 5. URL Structure

| URL | View | Name |
|-----|------|------|
| `/` | ProductListView | `store:product-list` |
| `/category/<slug>/` | ProductListView (filtered) | `store:category` |
| `/product/<slug>/` | ProductDetailView | `store:product-detail` |
| `/cart/` | cart_view | `store:cart` |
| `/cart/add/<pk>/` | cart_add | `store:cart-add` |
| `/cart/remove/<pk>/` | cart_remove | `store:cart-remove` |
| `/checkout/` | checkout_view | `store:checkout` |
| `/orders/` | order_list | `store:order-list` |
| `/orders/<pk>/` | order_detail | `store:order-detail` |

## 6. Acceptance Criteria

- [ ] Adding a product to the cart persists across page navigations (session)
- [ ] Checkout creates an Order and OrderItem records
- [ ] Stock is decremented on successful checkout
- [ ] Admin can see all orders with their items
- [ ] At least 10 tests pass

## 7. Out of Scope

- Payment gateway integration (Stripe)
- Email confirmation
