from decimal import Decimal


class Cart:
    """A session-based shopping cart."""

    def __init__(self, request):
        self.session = request.session
        self.cart    = self.session.setdefault('cart', {})

    def add(self, product, quantity=1, override=False):
        pid   = str(product.pk)
        entry = self.cart.setdefault(pid, {'quantity': 0, 'price': str(product.price)})
        if override:
            entry['quantity'] = quantity
        else:
            entry['quantity'] += quantity
        self.save()

    def remove(self, product):
        self.cart.pop(str(product.pk), None)
        self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session['cart']

    def __len__(self):
        return sum(i['quantity'] for i in self.cart.values())

    def __iter__(self):
        from .models import Product
        pks      = [int(k) for k in self.cart]
        products = Product.objects.filter(pk__in=pks)
        cart     = {str(p.pk): p for p in products}
        for pid, item in self.cart.items():
            item = item.copy()
            item['product']     = cart[pid]
            item['total_price'] = Decimal(item['price']) * item['quantity']
            yield item

    @property
    def total_price(self):
        return sum(Decimal(i['price']) * i['quantity'] for i in self.cart.values())
