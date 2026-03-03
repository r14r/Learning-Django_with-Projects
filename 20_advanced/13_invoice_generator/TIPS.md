# Tips & Implementation Guide: Invoice Generator

## 1. Total Calculation Properties

```python
class Invoice(models.Model):
    @property
    def subtotal(self):
        return sum(i.total for i in self.items.all())

    @property
    def tax_amount(self):
        return self.subtotal * self.tax_rate

    @property
    def total(self):
        return self.subtotal + self.tax_amount
```

## 2. PDF Generation with WeasyPrint

```bash
pip install weasyprint
```

```python
from django.template.loader import render_to_string
from weasyprint import HTML

def invoice_pdf(request, pk):
    invoice  = get_object_or_404(Invoice, pk=pk, owner=request.user)
    html_str = render_to_string('invoice_generator/invoice_pdf.html', {'invoice': invoice})
    pdf      = HTML(string=html_str, base_url=request.build_absolute_uri()).write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice-{invoice.number}.pdf"'
    return response
```

## 3. Auto-generate Invoice Number

```python
def generate_invoice_number():
    import uuid
    return f'INV-{uuid.uuid4().hex[:8].upper()}'
```
