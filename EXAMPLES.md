# Usage Examples & Best Practices

Real-world examples and best practices for using the Django Reusable Components Library.

## Table of Contents

- [Complete Blog Example](#complete-blog-example)
- [E-commerce Product Catalog](#e-commerce-product-catalog)
- [User Profile System](#user-profile-system)
- [Social Media Feed](#social-media-feed)
- [Dashboard with Widgets](#dashboard-with-widgets)
- [Best Practices](#best-practices)
- [Performance Optimization](#performance-optimization)
- [Common Patterns](#common-patterns)

---

## Complete Blog Example

A full-featured blog using rendertag, pagination, and renderblock.

### Models

```python
# blog/models.py
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    published_date = models.DateTimeField()
    featured_image = models.ImageField(upload_to='articles/')
    views = models.IntegerField(default=0)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_date']
```

### Views

```python
# blog/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Article, Category, Comment
from renderblock.renderblock import render_block_to_string
from django.http import JsonResponse

def article_list(request):
    """List all published articles with pagination"""
    articles = Article.objects.filter(published_date__lte=timezone.now())

    # Filter by category if specified
    category_slug = request.GET.get('category')
    if category_slug:
        articles = articles.filter(category__slug=category_slug)

    return render(request, 'blog/article_list.html', {
        'articles': articles,
        'categories': Category.objects.all(),
    })

def article_detail(request, slug):
    """Display single article with comments"""
    article = get_object_or_404(Article, slug=slug)

    # Increment view count
    article.views += 1
    article.save(update_fields=['views'])

    return render(request, 'blog/article_detail.html', {
        'article': article,
        'related_articles': Article.objects.filter(
            category=article.category
        ).exclude(id=article.id)[:5],
    })

@login_required
def add_comment(request, article_id):
    """AJAX endpoint to add comment"""
    if request.method == 'POST':
        article = get_object_or_404(Article, id=article_id)

        comment = Comment.objects.create(
            article=article,
            author=request.user,
            content=request.POST.get('content')
        )

        # Render just the comments section
        html = render_block_to_string(
            'blog/article_detail.html',
            'comments_block',
            {'article': article}
        )

        return JsonResponse({'success': True, 'html': html})

    return JsonResponse({'success': False})
```

### Templates

**blog/article_list.html**:
```django
{% extends 'base.html' %}
{% load makeobjectlist paginator render %}

{% block content %}
<div class="blog-header">
    <h1>Blog Articles</h1>

    <!-- Category filter -->
    <div class="categories">
        <a href="?" class="category-link">All</a>
        {% for category in categories %}
            <a href="?category={{ category.slug }}" class="category-link">
                {{ category.name }}
            </a>
        {% endfor %}
    </div>
</div>

<!-- Paginate articles -->
{% makeobjectlist articles paginate_by=12 %}

<!-- Article grid -->
<div class="articles-grid">
    {% for article in object_list %}
        {% render article templatetype="card" %}
    {% endfor %}
</div>

<!-- Pagination -->
<div class="pagination-wrapper">
    {% paginator %}
</div>
{% endblock %}
```

**templates/components/article_card.html**:
```django
<article class="article-card">
    <a href="{% url 'article_detail' object.slug %}">
        {% if object.featured_image %}
            <img src="{{ object.featured_image.url }}" alt="{{ object.title }}">
        {% endif %}

        <div class="card-content">
            <span class="category">{{ object.category.name }}</span>
            <h3>{{ object.title }}</h3>
            <p class="excerpt">{{ object.excerpt }}</p>

            <div class="meta">
                {% render object.author templatetype="mini" %}
                <span class="date">{{ object.published_date|date:"M d, Y" }}</span>
                <span class="views">{{ object.views }} views</span>
            </div>
        </div>
    </a>
</article>
```

**templates/components/article.html** (full article):
```django
<article class="article-full">
    <header>
        <span class="category">{{ object.category.name }}</span>
        <h1>{{ object.title }}</h1>

        <div class="article-meta">
            {% render object.author templatetype="byline" %}
            <time datetime="{{ object.published_date|date:'c' }}">
                {{ object.published_date|date:"F d, Y" }}
            </time>
            <span class="reading-time">5 min read</span>
        </div>
    </header>

    {% if object.featured_image %}
        <img src="{{ object.featured_image.url }}" alt="{{ object.title }}" class="featured-image">
    {% endif %}

    <div class="article-content">
        {{ object.content|safe }}
    </div>

    <footer>
        <div class="share">Share this article</div>
        <div class="tags">
            <!-- Tags here -->
        </div>
    </footer>
</article>
```

**blog/article_detail.html**:
```django
{% extends 'base.html' %}
{% load render %}

{% block content %}
<div class="article-container">
    <!-- Main article -->
    {% render article %}

    <!-- Comments section (for AJAX updates) -->
    {% block comments_block %}
    <section class="comments" id="comments">
        <h2>Comments ({{ article.comments.count }})</h2>

        {% if user.is_authenticated %}
        <form id="comment-form" class="comment-form" data-article="{{ article.id }}">
            {% csrf_token %}
            <textarea name="content" placeholder="Add a comment..." required></textarea>
            <button type="submit">Post Comment</button>
        </form>
        {% endif %}

        <div class="comments-list">
            {% for comment in article.comments.all %}
                {% render comment %}
            {% endfor %}
        </div>
    </section>
    {% endblock %}

    <!-- Related articles -->
    <aside class="related">
        <h3>Related Articles</h3>
        {% for related in related_articles %}
            {% render related templatetype="compact" %}
        {% endfor %}
    </aside>
</div>

<script>
// AJAX comment submission
$('#comment-form').submit(function(e) {
    e.preventDefault();

    $.post('/blog/add-comment/' + $(this).data('article') + '/', $(this).serialize(), function(data) {
        if (data.success) {
            $('#comments').replaceWith(data.html);
        }
    });
});
</script>
{% endblock %}
```

**templates/components/comment.html**:
```django
<div class="comment">
    <div class="comment-header">
        {% render object.author templatetype="avatar" %}
        <div class="comment-info">
            <span class="author-name">{{ object.author.username }}</span>
            <time datetime="{{ object.created_date|date:'c' }}">
                {{ object.created_date|timesince }} ago
            </time>
        </div>
    </div>
    <div class="comment-content">
        {{ object.content|linebreaks }}
    </div>
</div>
```

**templates/components/user_mini.html**:
```django
<span class="user-mini">
    <img src="{{ object.profile.avatar }}" alt="{{ object.username }}" width="20">
    {{ object.username }}
</span>
```

**templates/components/user_byline.html**:
```django
<div class="author-byline">
    <img src="{{ object.profile.avatar }}" alt="{{ object.username }}">
    <div>
        <span class="author-name">{{ object.get_full_name|default:object.username }}</span>
        <span class="author-bio">{{ object.profile.bio|truncatewords:15 }}</span>
    </div>
</div>
```

### URL Configuration

```python
# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('<slug:slug>/', views.article_detail, name='article_detail'),
    path('add-comment/<int:article_id>/', views.add_comment, name='add_comment'),
]
```

---

## E-commerce Product Catalog

Product listing with filtering and cart preview.

### Models

```python
# shop/models.py
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)

    def get_rating(self):
        # Calculate average rating
        return 4.5
```

### Views

```python
# shop/views.py
def product_list(request):
    products = Product.objects.filter(in_stock=True)

    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # Filter by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Sort
    sort = request.GET.get('sort', 'name')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')

    return render(request, 'shop/product_list.html', {
        'products': products,
        'categories': Category.objects.all(),
    })
```

### Templates

**shop/product_list.html**:
```django
{% extends 'base.html' %}
{% load makeobjectlist paginator render %}

{% block content %}
<div class="shop-container">
    <!-- Sidebar filters -->
    <aside class="shop-sidebar">
        <h3>Categories</h3>
        <ul>
            {% for category in categories %}
            <li>
                <a href="?category={{ category.slug }}">
                    {{ category.name }}
                </a>
            </li>
            {% endfor %}
        </ul>

        <h3>Price Range</h3>
        <form method="get">
            <input type="number" name="min_price" placeholder="Min">
            <input type="number" name="max_price" placeholder="Max">
            <button type="submit">Filter</button>
        </form>
    </aside>

    <!-- Product grid -->
    <main class="shop-main">
        <div class="shop-header">
            <h1>Products</h1>

            <select name="sort" onchange="location.href='?sort='+this.value">
                <option value="name">Name</option>
                <option value="price_low">Price: Low to High</option>
                <option value="price_high">Price: High to Low</option>
            </select>
        </div>

        {% makeobjectlist products paginate_by=24 %}

        <div class="products-grid">
            {% for product in object_list %}
                {% render product templatetype="card" %}
            {% endfor %}
        </div>

        {% paginator %}
    </main>
</div>
{% endblock %}
```

**templates/components/product_card.html**:
```django
<div class="product-card" data-product-id="{{ object.id }}">
    <a href="{% url 'product_detail' object.slug %}">
        <img src="{{ object.image.url }}" alt="{{ object.name }}">

        <div class="product-info">
            <h3>{{ object.name }}</h3>

            <div class="product-rating">
                {% with rating=object.get_rating %}
                    <span class="stars">★★★★☆</span>
                    <span class="rating-value">{{ rating }}</span>
                {% endwith %}
            </div>

            <div class="product-price">
                ${{ object.price }}
            </div>
        </div>
    </a>

    <button class="add-to-cart" data-product-id="{{ object.id }}">
        Add to Cart
    </button>
</div>
```

---

## User Profile System

User profiles with activity feed and follower system.

### Models

```python
# profiles/models.py
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', default='default-avatar.png')
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)

    def follower_count(self):
        return self.followers.count()

    def following_count(self):
        return self.user.following.count()

class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('post', 'Posted'),
        ('like', 'Liked'),
        ('comment', 'Commented'),
        ('follow', 'Followed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']
```

### Views

```python
# profiles/views.py
def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)

    return render(request, 'profiles/profile.html', {
        'profile_user': profile_user,
        'activities': profile_user.activities.all(),
    })

def user_followers(request, username):
    user = get_object_or_404(User, username=username)
    followers = user.profile.followers.all()

    return render(request, 'profiles/followers.html', {
        'profile_user': user,
        'followers': followers,
    })
```

### Templates

**profiles/profile.html**:
```django
{% extends 'base.html' %}
{% load render makeobjectlist paginator %}

{% block content %}
<div class="profile-container">
    <!-- Profile header -->
    <header class="profile-header">
        {% render profile_user.profile %}
    </header>

    <!-- Activity feed -->
    <section class="activity-feed">
        <h2>Recent Activity</h2>

        {% makeobjectlist activities paginate_by=20 %}

        <div class="activities">
            {% for activity in object_list %}
                {% render activity %}
            {% endfor %}
        </div>

        {% paginator %}
    </section>
</div>
{% endblock %}
```

**templates/components/userprofile.html**:
```django
<div class="profile-card">
    <img src="{{ object.avatar.url }}" alt="{{ object.user.username }}" class="avatar-large">

    <h1>{{ object.user.get_full_name|default:object.user.username }}</h1>

    <p class="bio">{{ object.bio }}</p>

    <div class="profile-stats">
        <div class="stat">
            <strong>{{ object.follower_count }}</strong>
            <span>Followers</span>
        </div>
        <div class="stat">
            <strong>{{ object.following_count }}</strong>
            <span>Following</span>
        </div>
    </div>

    {% if object.website %}
    <a href="{{ object.website }}" class="website">{{ object.website }}</a>
    {% endif %}

    {% if user.is_authenticated and user != object.user %}
    <button class="follow-button" data-user-id="{{ object.user.id }}">
        Follow
    </button>
    {% endif %}
</div>
```

**templates/components/activity.html**:
```django
<div class="activity">
    {% render object.user templatetype="avatar" %}

    <div class="activity-content">
        <span class="activity-text">
            <strong>{{ object.user.username }}</strong>
            {{ object.get_activity_type_display|lower }}
        </span>

        <div class="activity-details">
            {{ object.content|safe }}
        </div>

        <time datetime="{{ object.created_date|date:'c' }}">
            {{ object.created_date|timesince }} ago
        </time>
    </div>
</div>
```

---

## Best Practices

### 1. Template Organization

**Recommended structure**:
```
templates/
├── base.html
├── components/          # Object templates
│   ├── user.html
│   ├── user_mini.html
│   ├── user_avatar.html
│   ├── article.html
│   ├── article_card.html
│   ├── comment.html
│   └── ...
├── blog/               # Page templates
│   ├── article_list.html
│   ├── article_detail.html
│   └── ...
└── includes/           # Reusable snippets
    ├── header.html
    ├── footer.html
    └── ...
```

### 2. Template Naming Convention

Use descriptive postfixes:
- `_card`: Grid/card view
- `_compact`: Condensed view
- `_mini`: Minimal view
- `_full`: Full detail view
- `_avatar`: Profile picture only
- `_byline`: Author attribution

### 3. Context Management

Always use context push/pop for nested renders:

```python
# Good: rendertag handles this automatically
{% render object %}

# Avoid: Manual context manipulation
{% with foo=bar %}
    {% render object %}
{% endwith %}
```

### 4. Performance Optimization

**Select related data**:
```python
# Bad: N+1 queries
articles = Article.objects.all()

# Good: Prefetch related
articles = Article.objects.select_related('author', 'category').all()
```

**Use queryset caching**:
```python
# Bad: Hits DB twice
{% makeobjectlist articles paginate_by=10 %}
Total: {{ articles.count }}

# Good: Cache the queryset
{% with article_count=articles.count %}
{% makeobjectlist articles paginate_by=10 %}
Total: {{ article_count }}
{% endwith %}
```

### 5. AJAX Best Practices

**Use renderblock for partial updates**:
```python
# Return only what changed
def update_section(request):
    html = render_block_to_string('page.html', 'section_name', context)
    return JsonResponse({'html': html})
```

**Progressive enhancement**:
```django
<!-- Works without JS -->
<form method="post" action="/submit/" class="ajax-form">
    <!-- form fields -->
    <button type="submit">Submit</button>
</form>

<script>
// Enhance with AJAX
$('.ajax-form').submit(function(e) {
    e.preventDefault();
    // AJAX logic
});
</script>
```

### 6. Error Handling

**Graceful degradation**:
```django
{% render object %}
{# If template missing, shows error message but doesn't break page #}
```

**Custom error templates**:
```django
<!-- components/fallback.html -->
<div class="render-error">
    <p>Unable to display {{ object_type }}</p>
</div>
```

### 7. Security

**Never use user input in addition_filter**:
```django
<!-- UNSAFE -->
{% makeobjectlist articles addition_filter=request.GET.filter %}

<!-- SAFE: Filter in view -->
<!-- View code filters, template just paginates -->
{% makeobjectlist articles paginate_by=10 %}
```

### 8. Testing

**Test template rendering**:
```python
from django.test import TestCase
from django.template import Template, Context

class RenderTagTest(TestCase):
    def test_user_render(self):
        user = User.objects.create(username='test')
        template = Template('{% load render %}{% render user %}')
        html = template.render(Context({'user': user}))

        self.assertIn('test', html)
        self.assertIn('user', html)
```

---

## Performance Optimization

### Database Query Optimization

```python
# Before: N+1 query problem
articles = Article.objects.all()  # 1 query
for article in articles:
    print(article.author.username)  # N queries

# After: Select related
articles = Article.objects.select_related('author').all()  # 1 query
for article in articles:
    print(article.author.username)  # No extra queries

# For many-to-many
articles = Article.objects.prefetch_related('tags').all()
```

### Template Fragment Caching

```django
{% load cache %}

{% cache 600 article_sidebar article.id %}
    {% render article templatetype="sidebar" %}
{% endcache %}
```

### Pagination Optimization

```python
# Use paginator.count with caution on large tables
# Consider approximating for very large datasets

# Good for reasonable sizes
paginator = Paginator(objects, 25)

# For huge tables, consider cursor-based pagination
# or limit max page display
```

---

## Common Patterns

### Pattern: Master-Detail

```django
<!-- List page -->
{% for item in items %}
    {% render item templatetype="preview" %}
{% endfor %}

<!-- Detail page -->
{% render item %}  <!-- Uses full template -->
```

### Pattern: Nested Components

```django
<!-- components/article.html -->
<article>
    <h1>{{ object.title }}</h1>
    {% render object.author templatetype="byline" %}

    <div class="content">{{ object.content }}</div>

    <section class="comments">
        {% for comment in object.comments.all %}
            {% render comment %}
        {% endfor %}
    </section>
</article>
```

### Pattern: Conditional Rendering

```django
{% if user.is_authenticated %}
    {% render user templatetype="full" %}
{% else %}
    {% render user templatetype="public" %}
{% endif %}
```

### Pattern: Dynamic Component Selection

```python
# View
def render_dashboard_widget(request, widget_type):
    widget_data = get_widget_data(widget_type)
    return render(request, 'dashboard.html', {
        'widget': widget_data,
        'widget_type': widget_type,
    })
```

```django
<!-- Template -->
{% render widget templatetype=widget_type %}
```

---

Last updated: 2025-11-06
