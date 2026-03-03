# Step 2 – Models: Room and Message

```python
class Room(models.Model):
    name       = models.CharField(max_length=100, unique=True)
    slug       = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    room      = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    author    = models.ForeignKey(User, on_delete=models.CASCADE)
    content   = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['timestamp']
```
