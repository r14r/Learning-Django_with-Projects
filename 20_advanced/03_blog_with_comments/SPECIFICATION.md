# Specification: Blog with Comments

**Level:** Advanced  
**Project:** 03_blog_with_comments  
**Description:** Blog with user comments, pagination and tags

---

## 1. Overview

Build a full-featured blog where authors can publish posts, readers can leave
comments, and content is organised with tags and categories.

## 2. Goals

- Model posts with many-to-many tags and a status workflow (draft → published)
- Build paginated list and detail views
- Allow authenticated users to post comments
- Implement a tag cloud and related-posts sidebar

## 3. Functional Requirements

| # | Feature | Priority |
|---|---------|----------|
| 1 | Post list (paginated, newest first) | Must |
| 2 | Post detail with full body | Must |
| 3 | Comments on posts (authenticated) | Must |
| 4 | Tags on posts (many-to-many) | Must |
| 5 | Draft / published status (only published visible) | Must |
| 6 | Filter posts by tag | Should |
| 7 | Author profile page | Should |
| 8 | Markdown body rendering | Could |

## 4. Data Model

```
Tag
├── id   : AutoField
├── name : CharField(max_length=50, unique=True)
└── slug : SlugField(unique=True)

Post
├── id         : AutoField
├── title      : CharField(max_length=250)
├── slug       : SlugField(unique_for_date='publish')
├── author     : ForeignKey(User)
├── body       : TextField
├── image      : ImageField(upload_to='posts/', blank=True)
├── tags       : ManyToManyField(Tag, blank=True)
├── status     : CharField choices=[draft, published]
├── publish    : DateTimeField
└── created_at : DateTimeField(auto_now_add=True)

Comment
├── id         : AutoField
├── post       : ForeignKey(Post, related_name='comments')
├── author     : ForeignKey(User)
├── body       : TextField
├── active     : BooleanField(default=True)
└── created_at : DateTimeField(auto_now_add=True)
```

## 5. URL Structure

| URL | View | Name |
|-----|------|------|
| `/` | PostListView | `blog:list` |
| `/tag/<slug>/` | PostListView (filtered) | `blog:tag` |
| `/post/<year>/<month>/<day>/<slug>/` | PostDetailView | `blog:detail` |
| `/post/<pk>/comment/` | add_comment | `blog:add-comment` |

## 6. Acceptance Criteria

- [ ] Only published posts appear in the public list
- [ ] Comments require login; active=False comments hidden
- [ ] Pagination works with 5 posts per page
- [ ] Tag filter shows only posts with that tag
- [ ] At least 10 tests pass
