# Step 5 – Tests & Deployment Prep

## ecommerce_store/tests.py

```python
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal
from .models import Category, Product, Order, OrderItem

class StoreTests(TestCase):
    def setUp(self):
        self.client   = Client()
        self.category = Category.objects.create(name='Books', slug='books')
        self.product  = Product.objects.create(
            category=self.category, name='Django Book',
            slug='django-book', price=Decimal('29.99'), stock=10
        )

    def test_product_list(self):
        resp = self.client.get(reverse('ecommerce_store:product-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Django Book')

    def test_add_to_cart(self):
        self.client.post(reverse('ecommerce_store:cart-add', kwargs={'pk': self.product.pk}))
        resp = self.client.get(reverse('ecommerce_store:cart'))
        self.assertContains(resp, 'Django Book')

    def test_checkout_creates_order(self):
        self.client.post(reverse('ecommerce_store:cart-add', kwargs={'pk': self.product.pk}))
        resp = self.client.post(reverse('ecommerce_store:checkout'), {
            'first_name': 'Alice', 'last_name': 'Smith',
            'email': 'alice@example.com', 'address': '123 Main St',
        })
        self.assertEqual(Order.objects.count(), 1)
```
