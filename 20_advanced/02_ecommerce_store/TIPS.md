# Tips & Implementation Guide: E-Commerce Store

## 1. Session-Based Cart

Store the cart in `request.session` as a dict mapping product IDs to quantities:

```python
# cart.py
class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if cart is None:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        pid = str(product.pk)
        if pid not in self.cart:
            self.cart[pid] = {'quantity': 0, 'price': str(product.price)}
        self.cart[pid]['quantity'] += quantity
        self.save()

    def remove(self, product):
        pid = str(product.pk)
        if pid in self.cart:
            del self.cart[pid]
            self.save()

    def save(self):
        self.session.modified = True

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    @property
    def total_price(self):
        from decimal import Decimal
        return sum(Decimal(i['price']) * i['quantity'] for i in self.cart.values())
```

## 2. Models

```python
class Product(models.Model):
    category  = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name      = models.CharField(max_length=200)
    slug      = models.SlugField(unique=True)
    price     = models.DecimalField(max_digits=8, decimal_places=2)
    stock     = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    image     = models.ImageField(upload_to='products/', blank=True)
    ...
```

## 3. Checkout View

```python
def checkout_view(request):
    cart = Cart(request)
    if not cart:
        return redirect('store:product-list')
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            for pid, item in cart.cart.items():
                product = Product.objects.get(pk=pid)
                OrderItem.objects.create(
                    order=order, product=product,
                    price=item['price'], quantity=item['quantity']
                )
                product.stock -= item['quantity']
                product.save()
            del request.session['cart']
            return redirect('store:order-detail', pk=order.pk)
    else:
        form = CheckoutForm()
    return render(request, 'ecommerce_store/checkout.html', {'cart': cart, 'form': form})
```

## 4. Common Pitfalls

| Pitfall | Solution |
|---------|---------|
| Forgetting `session.modified = True` | Always call `cart.save()` after mutations |
| Not snapshotting price | Store price at order time, not a FK |
| Stock going negative | Wrap stock decrement in `select_for_update()` |
