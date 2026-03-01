# Step 4 – Forms & CRUD Operations

## What you'll add
Create, Update and Delete views with a ModelForm.

## chat_app/forms.py

```python
from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model  = Item
        fields = ['title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'title':       forms.TextInput(attrs={'class': 'form-control'}),
        }
```

## chat_app/views.py  (add to existing file)

```python
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import ItemForm

class ItemCreateView(LoginRequiredMixin, CreateView):
    model      = Item
    form_class = ItemForm
    success_url = reverse_lazy('chat_app:list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model      = Item
    form_class = ItemForm
    success_url = reverse_lazy('chat_app:list')

class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model       = Item
    success_url = reverse_lazy('chat_app:list')
```

## chat_app/urls.py  (updated)

```python
from django.urls import path
from . import views

app_name = 'chat_app'
urlpatterns = [
    path('',               views.ItemListView.as_view(),   name='list'),
    path('<int:pk>/',      views.ItemDetailView.as_view(), name='detail'),
    path('create/',        views.ItemCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.ItemUpdateView.as_view(), name='update'),
    path('<int:pk>/del/',  views.ItemDeleteView.as_view(), name='delete'),
]
```
