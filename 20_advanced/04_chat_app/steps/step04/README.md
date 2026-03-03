# Step 4 – HTTP Views, URLs and Templates

## chat_app/views.py

```python
class RoomListView(LoginRequiredMixin, ListView):
    model         = Room
    template_name = 'chat_app/room_list.html'
    context_object_name = 'rooms'

def room_view(request, slug):
    room     = get_object_or_404(Room, slug=slug)
    messages = room.messages.select_related('author').order_by('-timestamp')[:50]
    return render(request, 'chat_app/room.html', {
        'room': room, 'messages': reversed(list(messages)),
    })
```
