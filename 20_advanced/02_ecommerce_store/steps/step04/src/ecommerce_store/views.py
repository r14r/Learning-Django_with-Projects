from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .models import Category, Product, Order
from .forms import CheckoutForm, CartAddForm
from .cart import Cart


class ProductListView(ListView):
    model               = Product
    template_name       = 'ecommerce_store/product_list.html'
    context_object_name = 'products'
    paginate_by         = 12

    def get_queryset(self):
        qs = Product.objects.filter(available=True).select_related('category')
        slug = self.kwargs.get('slug')
        if slug:
            category = get_object_or_404(Category, slug=slug)
            qs = qs.filter(category=category)
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(name__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.all()
        return ctx


class ProductDetailView(DetailView):
    model         = Product
    slug_field    = 'slug'
    template_name = 'ecommerce_store/product_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['cart_form'] = CartAddForm()
        return ctx


def cart_view(request):
    cart = Cart(request)
    return render(request, 'ecommerce_store/cart.html', {'cart': cart})


def cart_add(request, pk):
    product = get_object_or_404(Product, pk=pk, available=True)
    form    = CartAddForm(request.POST or None)
    if form and form.is_valid():
        Cart(request).add(
            product,
            quantity=form.cleaned_data['quantity'],
            override=form.cleaned_data['override'],
        )
    else:
        Cart(request).add(product)
    return redirect('ecommerce_store:cart')


def cart_remove(request, pk):
    product = get_object_or_404(Product, pk=pk)
    Cart(request).remove(product)
    return redirect('ecommerce_store:cart')


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
                from .models import OrderItem
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


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'ecommerce_store/order_list.html', {'orders': orders})


def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'ecommerce_store/order_detail.html', {'order': order})