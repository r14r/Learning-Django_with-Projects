# Tips & Implementation Guide: Job Board

## 1. Role Detection

Use a simple property on User's profile or check for Company ownership:

```python
def is_employer(user):
    return hasattr(user, 'company')

@user_passes_test(is_employer)
def job_create(request):
    ...
```

## 2. Job Model

```python
class Job(models.Model):
    JOB_TYPES = [
        ('full_time', 'Full Time'), ('part_time', 'Part Time'),
        ('remote', 'Remote'), ('contract', 'Contract'),
    ]
    company     = models.ForeignKey(Company, on_delete=models.CASCADE)
    title       = models.CharField(max_length=200)
    location    = models.CharField(max_length=200)
    job_type    = models.CharField(max_length=20, choices=JOB_TYPES)
    salary_min  = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max  = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField()
    is_active   = models.BooleanField(default=True)
    posted_at   = models.DateTimeField(auto_now_add=True)
```

## 3. Search Filter

```python
def get_queryset(self):
    qs = Job.objects.filter(is_active=True).select_related('company')
    q  = self.request.GET.get('q')
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
    loc = self.request.GET.get('location')
    if loc:
        qs = qs.filter(location__icontains=loc)
    jtype = self.request.GET.get('type')
    if jtype:
        qs = qs.filter(job_type=jtype)
    return qs
```
