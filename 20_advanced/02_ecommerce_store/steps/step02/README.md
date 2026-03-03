# Step 2 – Models: Category, Product, Order

Add the data models and register them in the admin.

## ecommerce_store/models.py  (key excerpt)

```python
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    def __str__(self): return self.name

class Product(models.Model):
    category  = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name      = models.CharField(max_length=200)
    slug      = models.SlugField(unique=True)
    price     = models.DecimalField(max_digits=8, decimal_places=2)
    stock     = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    image     = models.ImageField(upload_to='products/', blank=True)
    created_at= models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name
```

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
