# API Reference

Complete API documentation for all components in the Django Reusable Components Library.

## Table of Contents

- [Template Tags](#template-tags)
  - [rendertag](#rendertag)
  - [paginatortag](#paginatortag)
  - [objectlisttag](#objectlisttag)
- [Utilities](#utilities)
  - [renderblock](#renderblock)
  - [generic_view_patch](#generic_view_patch)
- [Media Components](#media-components)
  - [blueprintcss](#blueprintcss)
  - [jquerylib](#jquerylib)
  - [lightbox](#lightbox)
- [GAE Components](#gae-components)
  - [PageRank](#pagerank)
  - [urlinfo](#urlinfo)
  - [sitemesh](#sitemesh)

---

## Template Tags

### rendertag

Automatically render Django objects using convention-based or custom templates.

#### Location
`rendertag/templatetags/render.py`

#### Tag Syntax

```django
{% load render %}

{% render object %}
{% render object template="path/to/template.html" %}
{% render object templatetype="postfix" %}
{% render list_of_objects %}
{% render list_of_objects listtemplate="path/to/list.html" %}
```

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `object` | Any | Yes | - | Object or list to render |
| `template` | String | No | `components/{classname}.html` | Custom template path |
| `templatetype` | String | No | None | Template postfix (e.g., "compact" → `{classname}_compact.html`) |
| `listtemplate` | String | No | Auto-detected | Template for rendering lists |

#### Supported Object Types

1. **Django Model Instances**
   - Automatically uses `components/{model_name}.html`
   - Example: `User` → `components/user.html`

2. **Lists/Querysets**
   - Auto-detects table vs. list format
   - Table if any item has `__len__` attribute
   - Otherwise renders as `<ul>`

3. **Dictionaries**
   - Renders key-value pairs

4. **Callable Objects**
   - Functions or methods are called first
   - Result is then rendered

5. **None**
   - Returns empty string

#### Context Variables

Templates receive:
- `object`: The object being rendered
- All variables from parent context (preserved via context push/pop)

#### Template Discovery

**Default Path**: `components/{classname}.html`

**With templatetype**: `components/{classname}_{templatetype}.html`

**With custom template**: Uses specified path

**Examples**:
```python
# User instance
{% render user %}
# → templates/components/user.html

# User with postfix
{% render user templatetype="compact" %}
# → templates/components/user_compact.html

# Custom template
{% render user template="profiles/card.html" %}
# → templates/profiles/card.html
```

#### Example Templates

**templates/components/user.html**:
```django
<div class="user">
    <img src="{{ object.avatar }}" alt="{{ object.username }}">
    <h3>{{ object.username }}</h3>
    <p>{{ object.email }}</p>
</div>
```

**templates/components/user_compact.html**:
```django
<span class="user-compact">
    <img src="{{ object.avatar }}" width="20">
    {{ object.username }}
</span>
```

**templates/components/article.html**:
```django
<article class="article">
    <h2>{{ object.title }}</h2>
    <p class="meta">
        By {% render object.author templatetype="compact" %}
        on {{ object.published_date|date:"Y-m-d" }}
    </p>
    <div class="content">
        {{ object.body|safe }}
    </div>
</article>
```

#### List Rendering

**Automatic List Detection**:
```django
{% render articles %}
<!-- If articles contain table-like data, renders: -->
<table>
    <tr><td>Article 1</td></tr>
    <tr><td>Article 2</td></tr>
</table>

<!-- Otherwise renders: -->
<ul>
    <li>Article 1</li>
    <li>Article 2</li>
</ul>
```

**Custom List Template**:
```django
{% render articles listtemplate="articles/grid.html" %}
```

**templates/articles/grid.html**:
```django
<div class="grid">
    {% for item in object %}
        {% render item templatetype="card" %}
    {% endfor %}
</div>
```

#### Advanced Usage

**Rendering Callable Objects**:
```python
# views.py
def get_featured_articles():
    return Article.objects.filter(featured=True)[:5]

context = {'get_featured': get_featured_articles}
```

```django
<!-- Template -->
{% render get_featured %}
<!-- Function is called, result is rendered -->
```

**Nested Rendering**:
```django
<!-- components/article.html -->
<article>
    <h2>{{ object.title }}</h2>
    {% render object.author templatetype="mini" %}
    {% render object.comments %}
</article>
```

#### Error Handling

- **Template not found**: Returns `[err: template {name} not found]`
- **None object**: Returns empty string
- **Invalid object**: Logs error, returns error message

#### Source Code Reference

- `RenderNode` class: `rendertag/templatetags/render.py:20`
- `do_render()` function: `rendertag/templatetags/render.py:100`
- `parse_args_kwargs_and_as_var()`: `rendertag/templatetags/render.py:150`

---

### paginatortag

Display Digg-style pagination with smart page range handling.

#### Location
`paginatortag/templatetags/paginator.py`

#### Tag Syntax

```django
{% load paginator %}

{% paginator %}
```

#### Required Context Variables

The tag expects these variables in the template context:

| Variable | Type | Description |
|----------|------|-------------|
| `page_obj` | Page | Django Page object from Paginator |
| `paginator` | Paginator | Django Paginator instance |

#### Configuration

**settings.py**:
```python
# Number of pages shown at the beginning
LEADING_PAGE_RANGE_DISPLAYED = 10  # Default: 10

# Number of pages shown around current page
ADJACENT_PAGES = 4  # Default: 4

# Number of pages shown at the end
TRAILING_PAGE_RANGE_DISPLAYED = 10  # Default: 10

# Pages outside the main range
NUM_PAGES_OUTSIDE_RANGE = 2  # Default: 2
```

#### Context Variables Set

The tag adds these to the template context:

| Variable | Type | Description |
|----------|------|-------------|
| `page_numbers` | List | List of page numbers to display (may include None for ellipsis) |
| `page` | Integer | Current page number |
| `pages` | Integer | Total number of pages |
| `has_next` | Boolean | Whether there's a next page |
| `has_previous` | Boolean | Whether there's a previous page |
| `page_obj` | Page | The page object (passed through) |
| `paginator` | Paginator | The paginator (passed through) |

#### Example Usage

**views.py**:
```python
from django.core.paginator import Paginator
from django.shortcuts import render

def article_list(request):
    articles = Article.objects.all().order_by('-published_date')

    paginator = Paginator(articles, 10)  # 10 items per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'articles/list.html', {
        'page_obj': page_obj,
        'paginator': paginator,
    })
```

**templates/articles/list.html**:
```django
{% load paginator %}

<h1>Articles</h1>

{% for article in page_obj %}
    <article>
        <h2>{{ article.title }}</h2>
        <p>{{ article.excerpt }}</p>
    </article>
{% endfor %}

<!-- Display pagination -->
{% paginator %}
```

#### Default Template

**paginatortag/templates/paginator.html**:
```django
{% if pages > 1 %}
<div class="pagination">
    {% if has_previous %}
        <a href="?page={{ page|add:"-1" }}" class="prev">&laquo; Previous</a>
    {% endif %}

    {% for page_num in page_numbers %}
        {% if page_num %}
            {% if page_num == page %}
                <span class="current">{{ page_num }}</span>
            {% else %}
                <a href="?page={{ page_num }}">{{ page_num }}</a>
            {% endif %}
        {% else %}
            <span class="ellipsis">...</span>
        {% endif %}
    {% endfor %}

    {% if has_next %}
        <a href="?page={{ page|add:"1" }}" class="next">Next &raquo;</a>
    {% endif %}
</div>
{% endif %}
```

#### Customizing the Template

1. **Copy default template**:
```bash
mkdir -p templates/paginatortag
cp paginatortag/templates/paginator.html templates/paginatortag/
```

2. **Customize** `templates/paginatortag/paginator.html`:
```django
{% if pages > 1 %}
<nav class="pagination" aria-label="Page navigation">
    <ul class="pagination-list">
        {% if has_previous %}
            <li><a href="?page=1" class="pagination-link">First</a></li>
            <li><a href="?page={{ page|add:"-1" }}" class="pagination-link">Previous</a></li>
        {% endif %}

        {% for page_num in page_numbers %}
            {% if page_num %}
                <li>
                    <a href="?page={{ page_num }}"
                       class="pagination-link {% if page_num == page %}is-current{% endif %}">
                        {{ page_num }}
                    </a>
                </li>
            {% else %}
                <li><span class="pagination-ellipsis">&hellip;</span></li>
            {% endif %}
        {% endfor %}

        {% if has_next %}
            <li><a href="?page={{ page|add:"1" }}" class="pagination-link">Next</a></li>
            <li><a href="?page={{ pages }}" class="pagination-link">Last</a></li>
        {% endif %}
    </ul>
</nav>
{% endif %}
```

#### Pagination Algorithm

The tag uses Digg-style pagination logic:

```
[1] [2] [3] ... [10] [11] [12] 13 [14] [15] [16] ... [98] [99] [100]
 ^                ^    ^    ^    ^   ^    ^    ^               ^
Leading range   Adjacent  Current  Adjacent         Trailing range
```

#### AJAX Pagination

```javascript
// jQuery example
$('.pagination a').click(function(e) {
    e.preventDefault();
    var url = $(this).attr('href');

    $.get(url, function(html) {
        var content = $(html).find('#content').html();
        $('#content').html(content);
    });
});
```

#### Source Code Reference

- `paginator` tag: `paginatortag/templatetags/paginator.py:1`

---

### objectlisttag

Create paginated object lists from Django querysets.

#### Location
`objectlisttag/templatetags/makeobjectlist.py`

#### Tag Syntax

```django
{% load makeobjectlist %}

{% makeobjectlist queryset paginate_by=10 %}
{% makeobjectlist queryset paginate_by=20 as custom_name %}
{% makeobjectlist queryset paginate_by=10 addition_filter=".filter(published=True)" %}
```

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `queryset` | QuerySet | Yes | - | Django queryset to paginate |
| `paginate_by` | Integer | No | 10 | Items per page |
| `addition_filter` | String | No | None | Additional filter chain (uses eval - **security risk**) |
| `as` | String | No | `object_list` | Variable name for results |

#### Context Variables Set

| Variable | Type | Description |
|----------|------|-------------|
| `object_list` | List | Paginated objects for current page |
| `page_obj` | Page | Django Page object |
| `paginator` | Paginator | Django Paginator instance |
| `page` | Integer | Current page number |

#### Example Usage

**Basic Pagination**:
```django
{% load makeobjectlist paginator %}

{% makeobjectlist articles paginate_by=10 %}

{% for article in object_list %}
    <h2>{{ article.title }}</h2>
{% endfor %}

{% paginator %}
```

**Custom Variable Name**:
```django
{% makeobjectlist Article.objects.all paginate_by=15 as all_articles %}

{% for article in all_articles %}
    <h2>{{ article.title }}</h2>
{% endfor %}
```

**With Additional Filter** (⚠️ **Security Warning**):
```django
<!-- WARNING: Uses eval() - only safe with trusted input -->
{% makeobjectlist articles paginate_by=10 addition_filter=".filter(published=True).order_by('-date')" %}
```

#### Complete Example

**views.py**:
```python
from django.shortcuts import render
from myapp.models import Article

def article_list(request):
    articles = Article.objects.all()
    return render(request, 'articles/list.html', {
        'articles': articles,
    })
```

**templates/articles/list.html**:
```django
{% load makeobjectlist paginator render %}

<h1>Articles</h1>

{# Paginate the queryset #}
{% makeobjectlist articles paginate_by=12 %}

{# Display articles #}
<div class="articles-grid">
    {% for article in object_list %}
        {% render article templatetype="card" %}
    {% endfor %}
</div>

{# Show pagination controls #}
<div class="pagination-wrapper">
    {% paginator %}
</div>
```

#### GET Parameter Handling

The tag automatically reads the `page` parameter from the URL:
- `/articles/` → Page 1
- `/articles/?page=2` → Page 2
- `/articles/?page=invalid` → Page 1 (graceful fallback)
- `/articles/?page=999` → Last page (graceful fallback)

#### Error Handling

- **Invalid page number**: Falls back to page 1
- **Page out of range**: Shows last page
- **Empty queryset**: Returns empty page

#### Security Considerations

⚠️ **WARNING**: The `addition_filter` parameter uses `eval()`:

```python
# In source code:
if addition_filter:
    object_list = eval('object_list' + addition_filter)
```

**Risks**:
- Code injection if user input reaches `addition_filter`
- Arbitrary code execution

**Mitigation**:
1. **Never** use user input in `addition_filter`
2. Only use hardcoded values in templates
3. For dynamic filtering, use view logic instead:

```python
# SAFE: Filter in view
def article_list(request):
    articles = Article.objects.all()

    category = request.GET.get('category')
    if category:
        articles = articles.filter(category=category)

    return render(request, 'list.html', {'articles': articles})
```

```django
<!-- SAFE: No eval -->
{% makeobjectlist articles paginate_by=10 %}
```

#### Source Code Reference

- `makeobjectlist` tag: `objectlisttag/templatetags/makeobjectlist.py:1`

---

## Utilities

### renderblock

Render individual template blocks without rendering the entire template.

#### Location
`renderblock/renderblock.py`

#### Functions

##### `render_block_to_string(template_name, block_name, context)`

Render a specific block from a template to a string.

**Parameters**:
- `template_name` (str): Template path
- `block_name` (str): Name of block to render
- `context` (dict): Context dictionary

**Returns**: String (rendered HTML)

**Raises**: `Exception` if block not found

**Example**:
```python
from renderblock.renderblock import render_block_to_string

html = render_block_to_string(
    'articles/detail.html',
    'comments_section',
    {'comments': comments}
)
```

##### `render_template_block(request, template_name, block_name, context_dict)`

Render a block and return HttpResponse.

**Parameters**:
- `request`: Django request object
- `template_name` (str): Template path
- `block_name` (str): Block name
- `context_dict` (dict): Context dictionary

**Returns**: HttpResponse

**Example**:
```python
from renderblock.renderblock import render_template_block

def ajax_comments(request, article_id):
    article = Article.objects.get(id=article_id)
    return render_template_block(
        request,
        'articles/detail.html',
        'comments_section',
        {'article': article, 'comments': article.comments.all()}
    )
```

##### `direct_block_to_template(request, template, block)`

View function for direct block rendering via URL.

**Parameters**:
- `request`: Django request object
- `template` (str): Template name (from URL)
- `block` (str): Block name (from URL)

**Returns**: HttpResponse

**URL Pattern**:
```python
# urls.py
from renderblock.renderblock import direct_block_to_template

urlpatterns = [
    url(r'^renderblock/(?P<template>[\w/]+)/(?P<block>\w+)/$',
        direct_block_to_template,
        name='render_block'),
]
```

**Usage**:
```
/renderblock/articles/detail/comments_section/
→ Renders 'comments_section' block from 'articles/detail.html'
```

#### Example Use Cases

**1. AJAX Partial Page Updates**:

```python
# views.py
from renderblock.renderblock import render_block_to_string
from django.http import JsonResponse

def update_sidebar(request):
    user = request.user
    html = render_block_to_string(
        'base.html',
        'sidebar',
        {'user': user}
    )
    return JsonResponse({'html': html})
```

```javascript
// JavaScript
$.get('/update-sidebar/', function(data) {
    $('#sidebar').html(data.html);
});
```

**2. Email Templates**:

```python
# utils.py
from renderblock.renderblock import render_block_to_string
from django.core.mail import send_mail

def send_welcome_email(user):
    # Use same template as web page
    html_content = render_block_to_string(
        'emails/welcome.html',
        'email_body',
        {'user': user}
    )

    send_mail(
        'Welcome!',
        'Welcome to our site',
        'noreply@example.com',
        [user.email],
        html_message=html_content
    )
```

**3. Template Block Testing**:

```python
# tests.py
from renderblock.renderblock import render_block_to_string

class TemplateBlockTests(TestCase):
    def test_user_card_block(self):
        user = User.objects.create(username='test')
        html = render_block_to_string(
            'components/user.html',
            'user_card',
            {'user': user}
        )
        self.assertIn('test', html)
        self.assertIn('user-card', html)
```

**4. Widget Rendering**:

```django
<!-- base.html -->
{% block weather_widget %}
<div class="weather">
    <h3>Weather</h3>
    <p>{{ weather.temp }}°C</p>
</div>
{% endblock %}

{% block news_widget %}
<div class="news">
    <h3>Latest News</h3>
    {% for item in news %}
        <p>{{ item.title }}</p>
    {% endfor %}
</div>
{% endblock %}
```

```python
# views.py - Render specific widgets
def weather_widget(request):
    return render_template_block(
        request,
        'base.html',
        'weather_widget',
        {'weather': get_weather()}
    )

def news_widget(request):
    return render_template_block(
        request,
        'base.html',
        'news_widget',
        {'news': News.objects.latest()[:5]}
    )
```

#### Block Extraction Algorithm

The function extracts blocks by:
1. Parsing template into node tree
2. Walking nodes to find BlockNode
3. Handling extends/include directives
4. Rendering specific block with context

Supports:
- Simple blocks
- Nested blocks
- Blocks in extended templates
- Conditional blocks

#### Source Code Reference

- `render_block_to_string()`: `renderblock/renderblock.py:50`
- `_get_block_from_template()`: `renderblock/renderblock.py:25`

---

### generic_view_patch

Enhanced Django generic views supporting extra form fields.

#### Location
`generic_view_patch/__init__.py`

#### Problem Solved

Standard Django generic views don't allow setting model fields not in the form:

```python
# Problem: How to set author field?
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']  # 'author' not in form!

# Article model has: author, title, content, created_date
```

#### Solution

Use `extra_fields` parameter to set additional fields:

```python
from generic_view_patch import create_object

url(r'^article/create/$', create_object, {
    'model': Article,
    'form_class': ArticleForm,
    'extra_fields': {
        'author': lambda request, obj: request.user,
        'created_date': lambda request, obj: datetime.now(),
    }
})
```

#### Functions

##### `create_object(**kwargs)`

Enhanced version of Django's `create_object` generic view.

**Additional Parameters**:
- `extra_fields` (dict): Field name → callable mapping

**Example**:
```python
from generic_view_patch import create_object
from myapp.models import BlogPost
from myapp.forms import BlogPostForm

urlpatterns = [
    url(r'^blog/create/$', create_object, {
        'model': BlogPost,
        'form_class': BlogPostForm,
        'template_name': 'blog/create.html',
        'extra_fields': {
            'author': lambda request, obj: request.user,
            'slug': lambda request, obj: slugify(obj.title),
            'created_date': lambda request, obj: timezone.now(),
        },
        'login_required': True,
    }),
]
```

##### `update_object(**kwargs)`

Enhanced version of Django's `update_object` generic view.

**Additional Parameters**:
- `extra_fields` (dict): Field name → callable mapping

**Example**:
```python
from generic_view_patch import update_object

urlpatterns = [
    url(r'^blog/(?P<object_id>\d+)/edit/$', update_object, {
        'model': BlogPost,
        'form_class': BlogPostForm,
        'template_name': 'blog/edit.html',
        'extra_fields': {
            'modified_by': lambda request, obj: request.user,
            'modified_date': lambda request, obj: timezone.now(),
        },
    }),
]
```

##### `apply_extra_fields_and_save(extra_fields, request, new_object)`

Helper function to apply extra fields.

**Parameters**:
- `extra_fields` (dict): Field name → callable
- `request`: Django request
- `new_object`: Model instance

**Returns**: None (modifies object in place)

**Example**:
```python
from generic_view_patch import apply_extra_fields_and_save

extra_fields = {
    'author': lambda request, obj: request.user,
    'ip_address': lambda request, obj: request.META.get('REMOTE_ADDR'),
}

article = Article(title="Test", content="Content")
apply_extra_fields_and_save(extra_fields, request, article)
# Now article.author and article.ip_address are set
```

#### Extra Fields Callable Signature

**Callable**: `func(request, obj) → value`

**Parameters**:
- `request`: Django HttpRequest
- `obj`: Model instance being created/updated

**Returns**: Value to assign to field

**Examples**:
```python
extra_fields = {
    # Simple lambda
    'author': lambda request, obj: request.user,

    # Access request data
    'ip_address': lambda request, obj: request.META.get('REMOTE_ADDR'),

    # Use object data
    'slug': lambda request, obj: slugify(obj.title),

    # Complex logic
    'category': lambda request, obj: (
        Category.objects.get(slug=request.POST.get('category'))
        if 'category' in request.POST
        else obj.category
    ),

    # Call function
    'token': lambda request, obj: generate_unique_token(),
}
```

#### Complete Example

```python
# models.py
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField(null=True)

# forms.py
from django import forms

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']  # Only user-editable fields

# urls.py
from django.contrib.auth.decorators import login_required
from generic_view_patch import create_object, update_object
from django.utils.text import slugify
from django.utils import timezone

urlpatterns = [
    url(r'^article/create/$',
        login_required(create_object),
        {
            'model': Article,
            'form_class': ArticleForm,
            'template_name': 'article_form.html',
            'post_save_redirect': '/articles/',
            'extra_fields': {
                'author': lambda request, obj: request.user,
                'slug': lambda request, obj: slugify(obj.title),
                'created_date': lambda request, obj: timezone.now(),
            },
        },
        name='article_create'
    ),

    url(r'^article/(?P<object_id>\d+)/edit/$',
        login_required(update_object),
        {
            'model': Article,
            'form_class': ArticleForm,
            'template_name': 'article_form.html',
            'post_save_redirect': '/articles/%(id)s/',
            'extra_fields': {
                'modified_date': lambda request, obj: timezone.now(),
            },
        },
        name='article_edit'
    ),
]
```

#### Modern Alternative: Class-Based Views

**Recommendation**: For Django 2.x+, use Class-Based Views instead:

```python
# views.py
from django.views.generic import CreateView, UpdateView
from django.utils.text import slugify
from django.utils import timezone

class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        form.instance.created_date = timezone.now()
        return super().form_valid(form)

# urls.py
from django.urls import path

urlpatterns = [
    path('article/create/', ArticleCreateView.as_view(), name='article_create'),
]
```

#### Source Code Reference

- `create_object()`: `generic_view_patch/__init__.py:50`
- `update_object()`: `generic_view_patch/__init__.py:75`
- `apply_extra_fields_and_save()`: `generic_view_patch/__init__.py:25`

---

## Media Components

### blueprintcss

Blueprint CSS framework integration.

#### Location
`blueprintcss/media/`

#### Files Included

| File | Size | Purpose |
|------|------|---------|
| `screen.css` | 11KB | Main stylesheet for screen |
| `print.css` | 1KB | Print-optimized styles |
| `ie.css` | 2KB | IE6/7/8 fixes |

#### Plugins

Located in `blueprintcss/media/plugins/`:

- **buttons**: Stylish CSS buttons
- **fancy-type**: Typography enhancements
- **link-icons**: Automatic link icons
- **rtl**: Right-to-left language support

#### Usage

```django
<!-- base.html -->
<link rel="stylesheet" href="{{ MEDIA_URL }}blueprintcss/media/screen.css" type="text/css" media="screen, projection">
<link rel="stylesheet" href="{{ MEDIA_URL }}blueprintcss/media/print.css" type="text/css" media="print">
<!--[if lt IE 8]>
<link rel="stylesheet" href="{{ MEDIA_URL }}blueprintcss/media/ie.css" type="text/css" media="screen, projection">
<![endif]-->
```

#### Grid System

Blueprint uses a 950px, 24-column grid:

```html
<div class="container">
    <div class="span-24">Full width</div>

    <div class="span-8">1/3 width</div>
    <div class="span-8">1/3 width</div>
    <div class="span-8 last">1/3 width</div>

    <div class="span-16">2/3 width</div>
    <div class="span-8 last">1/3 width</div>
</div>
```

#### Common Classes

- `.container`: Main container (950px)
- `.span-N`: Column width (N = 1-24)
- `.last`: Last column in row
- `.prepend-N`: Left margin
- `.append-N`: Right margin
- `.push-N` / `.pull-N`: Column reordering

#### Reference

- Blueprint documentation: http://www.blueprintcss.org/

---

### jquerylib

jQuery and essential plugins bundled.

#### Location
`jquerylib/media/`

#### Files Included

| File | Size | Description |
|------|------|-------------|
| `jquery.js` | 120KB | jQuery core library |
| `jquery.form.js` | 15KB | AJAX form submission |
| `jquery.livequery.js` | 8KB | Auto-bind dynamic elements |
| `jquery.bgiframe.js` | 2KB | IE z-index fixes |
| `jquery.ajax-queue.js` | 3KB | AJAX request queueing |
| `jquery.fixes.js` | 1KB | Custom jQuery fixes |

#### Usage

```django
<script src="{{ MEDIA_URL }}jquerylib/media/jquery.js"></script>
<script src="{{ MEDIA_URL }}jquerylib/media/jquery.form.js"></script>
<script src="{{ MEDIA_URL }}jquerylib/media/jquery.livequery.js"></script>
```

#### jquery.form Plugin

AJAX form submission:

```javascript
$('#myForm').ajaxForm({
    success: function(response) {
        alert('Form submitted!');
    },
    error: function() {
        alert('Error submitting form');
    }
});
```

#### jquery.livequery Plugin

Auto-bind to dynamic elements:

```javascript
// Bind to current and future .delete buttons
$('.delete').livequery(function() {
    $(this).click(function() {
        // Delete logic
    });
});
```

---

### lightbox

Sexy Lightbox v2.3 image viewer.

#### Location
`lightbox/media/`

#### Files

- `sexylightbox.v2.3.jquery.js`: Main plugin
- `jquery.easing.1.3.js`: Easing animations
- `sexylightbox.css`: Styles
- `images/`: Lightbox assets
- Themes: `black/`, `white/`

#### Basic Usage

```django
<!-- Include CSS -->
<link rel="stylesheet" href="{{ MEDIA_URL }}lightbox/media/sexylightbox.css">

<!-- Include JS (after jQuery) -->
<script src="{{ MEDIA_URL }}lightbox/media/jquery.easing.1.3.js"></script>
<script src="{{ MEDIA_URL }}lightbox/media/sexylightbox.v2.3.jquery.js"></script>

<!-- Initialize -->
<script>
$(function() {
    $('.gallery a').sexyLightbox();
});
</script>

<!-- HTML -->
<div class="gallery">
    <a href="large1.jpg" rel="gallery">
        <img src="thumb1.jpg" alt="Photo 1">
    </a>
    <a href="large2.jpg" rel="gallery">
        <img src="thumb2.jpg" alt="Photo 2">
    </a>
</div>
```

#### Options

```javascript
$('.gallery a').sexyLightbox({
    color: 'black',        // 'black' or 'white'
    dir: 'images/',        // Image directory
    slideSpeed: 200,       // Animation speed
    autoSize: true,        // Auto-resize
    counterText: '{x}/{y}' // Counter format
});
```

---

## GAE Components

### PageRank

Fetch Google PageRank scores (GAE-specific, deprecated).

#### Location
`PageRank/__init__.py`

#### Function

```python
get_pagerank(url)
```

**Parameters**:
- `url` (str): URL to check

**Returns**: Integer (0-10) or None

**Example**:
```python
from PageRank import get_pagerank

pr = get_pagerank('http://example.com')
if pr is not None:
    print(f"PageRank: {pr}/10")
```

#### Note

Uses deprecated Google Toolbar API. May not work reliably. Consider alternatives like Moz API or SEMrush.

---

### urlinfo

SEO metrics scraper (GAE-specific).

#### Location
`urlinfo/__init__.py`

#### URL Patterns

```python
/urlinfo/gpr/{url}           # Google PageRank
/urlinfo/gpages/{url}        # Google indexed pages
/urlinfo/glinks/{url}        # Google backlinks
/urlinfo/baidupages/{url}    # Baidu indexed pages
/urlinfo/baidu links/{url}    # Baidu backlinks
/urlinfo/yahoopages/{url}    # Yahoo pages
/urlinfo/yahooinlinks/{url}  # Yahoo inbound links
```

#### Example

```
GET /urlinfo/gpages/example.com
→ Returns: "About 1,234 results"

GET /urlinfo/glinks/example.com
→ Returns: "About 5,678 links"
```

#### Note

Uses screen scraping. Fragile and may break with search engine updates. Requires Google App Engine.

---

### sitemesh

Template composition with memcache (GAE-specific).

#### Location
`sitemesh/__init__.py`

#### Tag Syntax

```django
{% load sitemesh %}

{% loadurl url_or_view %}
{% loadurl url_or_view timeout %}
```

#### Parameters

- `url_or_view`: URL string or view function name
- `timeout`: Cache timeout in seconds (optional)

#### Example

```django
{% load sitemesh %}

<!-- Load external content (cached 1 hour) -->
{% loadurl "http://example.com/widget" 3600 %}

<!-- Load internal view -->
{% loadurl "/internal/sidebar/" %}

<!-- Load from view function -->
{% loadurl "myapp.views.get_sidebar" %}
```

#### Caching

Uses GAE memcache:
- Cache key: MD5 of URL
- Default timeout: No expiration
- Manual timeout: Specified in seconds

---

Last updated: 2025-11-06
