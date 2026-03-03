# Step 2 – Models: Label, Task, Comment

```python
class Label(models.Model):
    name  = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default='#6c757d')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Task(models.Model):
    STATUS   = [('todo','Todo'),('in_progress','In Progress'),('done','Done')]
    PRIORITY = [('low','Low'),('medium','Medium'),('high','High'),('critical','Critical')]
    title    = models.CharField(max_length=200)
    status   = models.CharField(max_length=20, choices=STATUS, default='todo')
    priority = models.CharField(max_length=10, choices=PRIORITY, default='medium')
    due_date = models.DateField(null=True, blank=True)
    owner    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_tasks')
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                  blank=True, related_name='assigned_tasks')
    labels   = models.ManyToManyField(Label, blank=True)
```
