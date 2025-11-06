# Installation Guide

This document provides detailed installation instructions for the Django Reusable Components Library.

## Table of Contents

- [Requirements](#requirements)
- [Installation Methods](#installation-methods)
- [Component Setup](#component-setup)
- [Configuration](#configuration)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

## Requirements

### Minimum Requirements

- Python 2.7+ (Python 3.x requires code migration - see MIGRATION.md)
- Django 1.0+ (Django 2.x+ requires updates)
- For GAE components: Google App Engine SDK

### Optional Dependencies

- **ragendja**: For media file combining (CSS/JS)
- **memcache**: For sitemesh caching on GAE
- **PIL/Pillow**: For image handling in lightbox

## Installation Methods

### Method 1: Direct Integration (Recommended)

1. **Copy components to your project**:

```bash
# Copy specific components you need
cp -r /path/to/Reusable/rendertag /your/project/
cp -r /path/to/Reusable/paginatortag /your/project/
cp -r /path/to/Reusable/objectlisttag /your/project/
```

2. **Add to INSTALLED_APPS**:

```python
# settings.py
INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    # ...

    # Reusable components
    'rendertag',
    'paginatortag',
    'objectlisttag',
    'renderblock',

    # Your apps
    'myapp',
]
```

### Method 2: Python Path

1. **Add to Python path**:

```python
# settings.py
import sys
sys.path.insert(0, '/path/to/Reusable')
```

2. **Add to INSTALLED_APPS** as shown in Method 1.

### Method 3: Symbolic Link

```bash
# Create symlink in your project
ln -s /path/to/Reusable/rendertag /your/project/rendertag
ln -s /path/to/Reusable/paginatortag /your/project/paginatortag
```

## Component Setup

### 1. Template Tags (rendertag, paginatortag, objectlisttag)

**Installation**:
```python
# settings.py
INSTALLED_APPS += [
    'rendertag',
    'paginatortag',
    'objectlisttag',
]
```

**Create template directories**:
```bash
# For rendertag
mkdir -p templates/components

# For paginatortag (optional, uses built-in template)
mkdir -p templates/paginatortag
```

**Template configuration**:
```python
# settings.py
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [
        os.path.join(BASE_DIR, 'templates'),
    ],
    'APP_DIRS': True,  # Important: enables app template loading
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.request',
            # ... other processors
        ],
    },
}]
```

**Pagination settings** (optional):
```python
# settings.py
# Customize pagination display
LEADING_PAGE_RANGE_DISPLAYED = 10  # Pages shown at start
ADJACENT_PAGES = 4                 # Pages around current page
TRAILING_PAGE_RANGE_DISPLAYED = 10 # Pages shown at end
NUM_PAGES_OUTSIDE_RANGE = 2        # Pages outside range
```

### 2. Blueprint CSS

**Installation**:
```python
# settings.py
INSTALLED_APPS += ['blueprintcss']

# Media configuration
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
```

**URL configuration**:
```python
# urls.py (Django 1.x)
from django.conf import settings

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

# urls.py (Django 2.x+)
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**Template usage**:
```django
<!-- base.html -->
<link rel="stylesheet" href="{{ MEDIA_URL }}blueprintcss/media/screen.css">
<link rel="stylesheet" href="{{ MEDIA_URL }}blueprintcss/media/print.css" media="print">
<!--[if lt IE 8]>
<link rel="stylesheet" href="{{ MEDIA_URL }}blueprintcss/media/ie.css">
<![endif]-->
```

### 3. jQuery Library

**Installation**:
```python
# settings.py
INSTALLED_APPS += ['jquerylib']
```

**Template usage**:
```django
<!-- base.html -->
<script src="{{ MEDIA_URL }}jquerylib/media/jquery.js"></script>
<script src="{{ MEDIA_URL }}jquerylib/media/jquery.form.js"></script>
<script src="{{ MEDIA_URL }}jquerylib/media/jquery.livequery.js"></script>
```

**With media combining** (ragendja):
```python
# settings.py
COMBINE_MEDIA = {
    'combined-js.js': (
        'jquerylib/media/jquery.js',
        'jquerylib/media/jquery.form.js',
        'jquerylib/media/jquery.livequery.js',
    ),
}
```

### 4. Lightbox

**Installation**:
```python
# settings.py
INSTALLED_APPS += ['lightbox']
```

**Template usage**:
```django
<!-- Include CSS -->
<link rel="stylesheet" href="{{ MEDIA_URL }}lightbox/media/sexylightbox.css">

<!-- Include JS (after jQuery) -->
<script src="{{ MEDIA_URL }}lightbox/media/jquery.easing.1.3.js"></script>
<script src="{{ MEDIA_URL }}lightbox/media/sexylightbox.v2.3.jquery.js"></script>

<!-- Initialize -->
<script>
$(function() {
    $('.gallery a').sexyLightbox({
        color: 'black'  // or 'white'
    });
});
</script>
```

### 5. renderblock

**Installation**:
```python
# settings.py
INSTALLED_APPS += ['renderblock']
```

**No additional configuration needed**. Use in views:
```python
from renderblock.renderblock import render_block_to_string
```

### 6. generic_view_patch

**Installation**:
```python
# No INSTALLED_APPS entry needed
# Just import and use in urls.py
```

**URL configuration**:
```python
# urls.py
from generic_view_patch import create_object, update_object
from myapp.models import Article
from myapp.forms import ArticleForm
from django.contrib.auth.decorators import login_required

urlpatterns += [
    url(r'^article/create/$',
        login_required(create_object),
        {
            'model': Article,
            'form_class': ArticleForm,
            'extra_fields': {
                'author': lambda request, obj: request.user,
            }
        },
        name='article_create'
    ),
]
```

### 7. GAE-Specific Components (PageRank, urlinfo, sitemesh)

**Requirements**:
- Google App Engine SDK
- app.yaml configuration

**Installation**:
```python
# settings.py (GAE)
INSTALLED_APPS += [
    'PageRank',
    'urlinfo',
    'sitemesh',
]
```

**URL configuration** (urlinfo):
```python
# urls.py
urlpatterns += [
    url(r'^urlinfo/', include('urlinfo.urls')),
]
```

**app.yaml** (GAE):
```yaml
application: your-app-id
version: 1
runtime: python27
api_version: 1

handlers:
- url: /urlinfo/.*
  script: main.py

- url: /media
  static_dir: media

libraries:
- name: django
  version: "1.2"
```

## Configuration

### Template Tag Configuration

#### rendertag

Create default templates in `templates/components/`:

```django
<!-- templates/components/user.html -->
<div class="user">
    <h3>{{ object.username }}</h3>
    <p>{{ object.email }}</p>
</div>

<!-- templates/components/user_compact.html -->
<span class="user-compact">{{ object.username }}</span>

<!-- templates/components/article.html -->
<article>
    <h2>{{ object.title }}</h2>
    <div class="content">{{ object.body|safe }}</div>
</article>
```

#### paginatortag

Customize the pagination template (optional):

```bash
# Copy default template
cp paginatortag/templates/paginator.html templates/paginatortag/paginator.html

# Edit templates/paginatortag/paginator.html
```

### Static File Configuration (Django 1.4+)

```python
# settings.py
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Collect static files
```

```bash
python manage.py collectstatic
```

### Media Files with Nginx

```nginx
# nginx.conf
location /media/ {
    alias /path/to/your/project/media/;
    expires 30d;
}

location /static/ {
    alias /path/to/your/project/staticfiles/;
    expires 30d;
}
```

## Verification

### Test Template Tags

```python
# Create test view
# views.py
from django.shortcuts import render
from django.contrib.auth.models import User

def test_rendertag(request):
    users = User.objects.all()[:5]
    return render(request, 'test_render.html', {'users': users})
```

```django
<!-- templates/test_render.html -->
{% load render %}

<h1>Test Render Tag</h1>
{% for user in users %}
    {% render user %}
{% endfor %}
```

### Test Pagination

```python
# views.py
from django.shortcuts import render
from myapp.models import Article

def test_pagination(request):
    articles = Article.objects.all()
    return render(request, 'test_pagination.html', {'articles': articles})
```

```django
<!-- templates/test_pagination.html -->
{% load makeobjectlist paginator %}

{% makeobjectlist articles paginate_by=10 %}

<h1>Articles</h1>
{% for article in object_list %}
    <p>{{ article.title }}</p>
{% endfor %}

{% paginator %}
```

### Test renderblock

```python
# views.py
from renderblock.renderblock import render_block_to_string
from django.http import HttpResponse

def test_renderblock(request):
    html = render_block_to_string('test_blocks.html', 'content', {
        'message': 'Hello from renderblock!'
    })
    return HttpResponse(html)
```

```django
<!-- templates/test_blocks.html -->
{% block content %}
<div>{{ message }}</div>
{% endblock %}
```

## Troubleshooting

### Issue: Template not found

**Problem**: `TemplateDoesNotExist: components/user.html`

**Solution**:
1. Ensure `APP_DIRS = True` in TEMPLATES settings
2. Create the template in `templates/components/`
3. Check INSTALLED_APPS includes the component app
4. Verify template directory structure

### Issue: Media files not loading

**Problem**: CSS/JS files return 404

**Solution**:
```python
# Check settings
print(settings.MEDIA_ROOT)
print(settings.MEDIA_URL)

# Verify files exist
ls -la media/blueprintcss/
ls -la media/jquerylib/

# Check URL configuration for development
# urls.py should include static serve pattern
```

### Issue: Import errors

**Problem**: `ImportError: No module named rendertag`

**Solution**:
1. Check Python path includes component directory
2. Verify __init__.py exists in component directory
3. Check INSTALLED_APPS configuration
4. Try absolute imports

### Issue: Context variable not available

**Problem**: `{{ object }}` is empty in rendered template

**Solution**:
- rendertag automatically provides `object` variable
- Check your template uses `{{ object.field }}` not `{{ user.field }}`
- Verify the object is not None

### Issue: Pagination not showing

**Problem**: Pagination doesn't display

**Solution**:
```python
# Check context has required variables
# Should have: page_obj, paginator

# In view, use Django's Paginator:
from django.core.paginator import Paginator

paginator = Paginator(object_list, 10)
page_obj = paginator.get_page(request.GET.get('page', 1))

return render(request, 'template.html', {
    'page_obj': page_obj,
    'paginator': paginator,
})
```

### Issue: GAE components fail

**Problem**: `ImportError: No module named google.appengine`

**Solution**:
- GAE components only work on Google App Engine
- For local development, use GAE dev_appserver
- Consider replacing with non-GAE alternatives

## Next Steps

- Read [COMPONENTS.md](COMPONENTS.md) for detailed component documentation
- See [MIGRATION.md](MIGRATION.md) for Python 3 / Django 2+ migration guide
- Check [README.md](README.md) for usage examples
- Review example templates in each component directory

## Getting Help

- Check component source code for docstrings
- Review git commit history for bug fixes
- See developer blog: http://robertmao.com

---

Last updated: 2025-11-06
