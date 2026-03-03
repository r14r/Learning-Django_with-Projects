# Step 3 – Product List, Detail & Session Cart

## cart.py

```python
class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.setdefault('cart', {})

    def add(self, product, quantity=1):
        pid = str(product.pk)
        entry = self.cart.setdefault(pid, {'quantity': 0, 'price': str(product.price)})
        entry['quantity'] += quantity
        self.save()

    def remove(self, product):
        self.cart.pop(str(product.pk), None)
        self.save()

    def save(self):
        self.session.modified = True

    def __len__(self):
        return sum(i['quantity'] for i in self.cart.values())
```
