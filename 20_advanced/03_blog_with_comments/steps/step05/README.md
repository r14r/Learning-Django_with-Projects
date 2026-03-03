# Step 5 – Tests & Deployment Prep

## tests.py

```python
class PostTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('alice', password='pass')
        self.post = Post.objects.create(
            title='Hello World', slug='hello-world', author=self.user,
            body='Test post body', status='published', publish=timezone.now()
        )

    def test_list_view(self):
        resp = self.client.get(reverse('blog_with_comments:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Hello World')

    def test_draft_not_visible(self):
        Post.objects.create(
            title='Draft Post', slug='draft-post', author=self.user,
            body='...', status='draft', publish=timezone.now()
        )
        resp = self.client.get(reverse('blog_with_comments:list'))
        self.assertNotContains(resp, 'Draft Post')
```
