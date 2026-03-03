# Step 4 – Checkout & Order History

## Checkout view (excerpt)

```python
def checkout_view(request):
    cart = Cart(request)
    if not cart:
        return redirect('ecommerce_store:product-list')
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order, product=item['product'],
                    price=item['price'], quantity=item['quantity'],
                )
                item['product'].stock -= item['quantity']
                item['product'].save()
            cart.clear()
            return redirect('ecommerce_store:order-detail', pk=order.pk)
    else:
        form = CheckoutForm()
    return render(request, 'ecommerce_store/checkout.html', {'cart': cart, 'form': form})
```
