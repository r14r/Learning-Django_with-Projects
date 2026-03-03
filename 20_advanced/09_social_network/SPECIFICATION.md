# Specification: Social Network

**Level:** Advanced  
**Project:** 09_social_network  
**Description:** User profiles, following, posts and likes

---

## 1. Overview

Build a mini social network where users have public profiles, can follow each other,
publish posts with photos, and like and comment on others' content.

## 2. Goals

- Extend Django's built-in User with a `Profile` model (one-to-one)
- Implement a follow/unfollow system
- Build a personalised feed showing posts from followed users
- Add like functionality with AJAX or a simple POST action

## 3. Functional Requirements

| # | Feature | Priority |
|---|---------|----------|
| 1 | User profile with bio and avatar | Must |
| 2 | Follow / unfollow other users | Must |
| 3 | Create posts with optional image | Must |
| 4 | Personal feed: posts from followed users | Must |
| 5 | Like / unlike a post | Must |
| 6 | Comment on posts | Should |
| 7 | Explore page (public posts) | Should |
| 8 | Notifications for new likes/follows | Could |

## 4. Data Model

```
Profile  (one-to-one with User)
├── bio       : TextField(blank=True)
├── avatar    : ImageField(upload_to='avatars/', blank=True)
├── website   : URLField(blank=True)
└── following : ManyToManyField(User, blank=True, symmetrical=False)

Post
├── id         : AutoField
├── author     : ForeignKey(User)
├── body       : TextField
├── image      : ImageField(upload_to='posts/', blank=True)
├── likes      : ManyToManyField(User, related_name='liked_posts', blank=True)
└── created_at : DateTimeField(auto_now_add=True)

Comment
├── id         : AutoField
├── post       : ForeignKey(Post, related_name='comments')
├── author     : ForeignKey(User)
├── body       : TextField
└── created_at : DateTimeField(auto_now_add=True)
```

## 5. URL Structure

| URL | View | Name |
|-----|------|------|
| `/` | FeedView | `social_network:feed` |
| `/explore/` | ExploreView | `social_network:explore` |
| `/profile/<username>/` | ProfileView | `social_network:profile` |
| `/profile/edit/` | ProfileEditView | `social_network:profile-edit` |
| `/post/create/` | PostCreateView | `social_network:post-create` |
| `/post/<pk>/delete/` | PostDeleteView | `social_network:post-delete` |
| `/post/<pk>/like/` | like_post | `social_network:like` |
| `/follow/<username>/` | follow_view | `social_network:follow` |

## 6. Acceptance Criteria

- [ ] Profile auto-created on user registration via signal
- [ ] Feed only shows posts from followed users (plus own posts)
- [ ] Follow/unfollow toggles work correctly
- [ ] Like count updates correctly
- [ ] At least 10 tests pass
