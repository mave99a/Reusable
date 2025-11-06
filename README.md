# Django Reusable Components Library

A collection of reusable Django apps and utilities that simplify common web development tasks. This library provides powerful template tags, CSS/JS framework integration, and SEO utilities.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Components](#components)
- [Requirements](#requirements)
- [License](#license)

## 🎯 Overview

This library contains battle-tested Django components designed to:

- **Simplify object rendering** with automatic template discovery
- **Streamline pagination** with smart page range handling
- **Integrate popular frameworks** (Blueprint CSS, jQuery)
- **Provide SEO utilities** (PageRank, URL information)
- **Enhance Django views** with flexible form handling

Originally developed for Google App Engine but most components work with any Django project.

## ✨ Features

### Core Template Tags

- **rendertag**: Automatically render Django objects using convention-based templates
- **paginatortag**: Display Digg-style pagination with smart page ranges
- **objectlisttag**: Create paginated object lists from querysets
- **renderblock**: Render individual template blocks for AJAX applications

### Framework Integration

- **blueprintcss**: Blueprint CSS framework with IE fixes and plugins
- **jquerylib**: jQuery with essential plugins (forms, livequery, AJAX queue)
- **lightbox**: Sexy lightbox image viewer integration

### Utilities

- **PageRank**: Fetch Google PageRank scores (GAE-specific)
- **urlinfo**: SEO metrics scraper (Google/Baidu/Yahoo indexing info)
- **sitemesh**: Template composition with memcache (GAE-specific)
- **generic_view_patch**: Enhanced Django generic views with extra_fields support

## 📦 Installation

### Basic Installation

1. Clone this repository:
```bash
git clone <repository-url>
```

2. Add desired components to your Django project's `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ... your apps
    'rendertag',
    'paginatortag',
    'objectlisttag',
    'renderblock',
    'blueprintcss',
    'jquerylib',
    'lightbox',
    # ... other components as needed
]
```

3. For media files (CSS/JS), ensure your `MEDIA_ROOT` and `MEDIA_URL` are configured properly.

### Component-Specific Setup

**For Blueprint CSS and jQuery:**
```python
# If using ragendja for media combining
from ragendja.settings_post import settings
```

**For GAE-specific components** (PageRank, urlinfo, sitemesh):
- Requires Google App Engine SDK
- Configure `app.yaml` accordingly

## 🚀 Quick Start

### Example 1: Render Objects Automatically

```python
# views.py
from myapp.models import User

def user_detail(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'user_detail.html', {'user': user})
```

```django
<!-- user_detail.html -->
{% load render %}

<!-- Automatically uses template: components/user.html -->
{% render user %}

<!-- Or specify a custom template -->
{% render user template="profiles/user_card.html" %}

<!-- Render with a specific type/postfix -->
{% render user templatetype="compact" %}  <!-- uses components/user_compact.html -->
```

### Example 2: Paginated Object Lists

```django
<!-- articles_list.html -->
{% load makeobjectlist paginator %}

<!-- Create paginated list from queryset -->
{% makeobjectlist articles paginate_by=10 %}

<!-- Display pagination UI -->
{% paginator %}

<!-- Iterate through paginated results -->
{% for article in object_list %}
    {% render article %}
{% endfor %}
```

### Example 3: Render Template Blocks for AJAX

```python
# views.py
from renderblock.renderblock import render_block_to_string

def get_sidebar(request):
    context = {'user': request.user}
    html = render_block_to_string('base.html', 'sidebar', context)
    return HttpResponse(html)
```

## 📚 Components

### 1. rendertag

**Purpose**: Automatically render Django objects using convention-based template discovery.

**Features**:
- Automatic template path: `components/{classname}.html`
- Support for custom templates
- Automatic list rendering in `<ul>` or `<table>`
- Template type/postfix support
- Callable object support
- Context preservation with push/pop

**Usage**:
```django
{% load render %}

<!-- Basic usage -->
{% render object_instance %}

<!-- Custom template -->
{% render object_instance template="custom/path.html" %}

<!-- List with custom template -->
{% render items_list listtemplate="custom_list.html" %}

<!-- Template with postfix -->
{% render user templatetype="compact" %}
```

**Template Creation**:
```django
<!-- components/user.html -->
<div class="user-card">
    <h3>{{ object.username }}</h3>
    <p>{{ object.email }}</p>
</div>
```

**Key Files**: `rendertag/templatetags/render.py:1`

### 2. paginatortag

**Purpose**: Display Digg-style pagination with smart page range handling.

**Features**:
- Smart pagination (shows adjacent pages + first/last)
- Configurable page ranges
- Automatic GET parameter handling
- Template-based rendering

**Configuration**:
```python
# Default settings
LEADING_PAGE_RANGE_DISPLAYED = 10  # Pages shown at start
ADJACENT_PAGES = 4                 # Pages shown around current
```

**Usage**:
```django
{% load paginator %}

<!-- Assumes page_obj and paginator in context -->
{% paginator %}
```

**Context Variables Provided**:
- `page_numbers`: List of page numbers to display
- `page`: Current page number
- `pages`: Total pages
- `has_next`: Boolean for next page
- `has_previous`: Boolean for previous page

**Key Files**: `paginatortag/templatetags/paginator.py:1`

### 3. objectlisttag

**Purpose**: Create paginated object lists from Django querysets.

**Features**:
- Paginate any Django queryset
- Custom per-page count
- Additional filter support
- Automatic page extraction from GET parameters
- Graceful error handling

**Usage**:
```django
{% load makeobjectlist %}

<!-- Basic pagination -->
{% makeobjectlist articles paginate_by=10 %}

<!-- With additional filter -->
{% makeobjectlist articles paginate_by=20 addition_filter=".filter(published=True)" %}

<!-- Store in custom variable -->
{% makeobjectlist articles paginate_by=10 as my_articles %}
```

**Key Files**: `objectlisttag/templatetags/makeobjectlist.py:1`

### 4. renderblock

**Purpose**: Render individual template blocks without rendering the entire template.

**Features**:
- Extract and render specific blocks
- Support for template inheritance
- Useful for AJAX partial page updates
- Handles nested and conditional blocks

**Usage**:
```python
from renderblock.renderblock import render_block_to_string

# Render a specific block
html = render_block_to_string('template.html', 'block_name', context_dict)

# In views
def ajax_sidebar(request):
    html = render_block_to_string('base.html', 'sidebar', {'user': request.user})
    return HttpResponse(html)
```

**Key Functions**:
- `render_block_to_string(template_name, block_name, context)`
- `direct_block_to_template(request, template, block)`

**Key Files**: `renderblock/renderblock.py:1`

### 5. blueprintcss

**Purpose**: Blueprint CSS framework integration for rapid prototyping.

**Includes**:
- `screen.css`: Main stylesheet (11KB)
- `print.css`: Print-optimized styles
- `ie.css`: Internet Explorer fixes
- Plugins: buttons, fancy-type, link-icons, RTL support

**Usage**:
```django
<!-- In your base template -->
<link rel="stylesheet" href="{{ MEDIA_URL }}blueprintcss/screen.css" type="text/css" media="screen, projection">
<link rel="stylesheet" href="{{ MEDIA_URL }}blueprintcss/print.css" type="text/css" media="print">
<!--[if lt IE 8]>
<link rel="stylesheet" href="{{ MEDIA_URL }}blueprintcss/ie.css" type="text/css" media="screen, projection">
<![endif]-->
```

### 6. jquerylib

**Purpose**: jQuery and essential plugins bundled for convenience.

**Includes**:
- jQuery core (120KB)
- jquery.form.js: AJAX form submission
- jquery.livequery.js: Auto-bind to dynamic elements
- jquery.bgiframe.js: IE z-index fixes
- jquery.ajax-queue.js: Queue AJAX requests
- jquery.fixes.js: Custom fixes

**Usage**:
```django
<script src="{{ MEDIA_URL }}jquerylib/jquery.js"></script>
<script src="{{ MEDIA_URL }}jquerylib/jquery.form.js"></script>
```

### 7. lightbox

**Purpose**: Sexy lightbox v2.3 image viewer for galleries.

**Includes**:
- sexylightbox.v2.3.jquery.js
- jquery.easing.1.3.js
- Themes: black, white
- CSS and image assets

**Usage**:
```django
<!-- Include CSS and JS -->
<link rel="stylesheet" href="{{ MEDIA_URL }}lightbox/sexylightbox.css">
<script src="{{ MEDIA_URL }}lightbox/sexylightbox.v2.3.jquery.js"></script>

<!-- Initialize -->
<script>
$(function() {
    $('.gallery a').sexyLightbox();
});
</script>

<!-- HTML -->
<div class="gallery">
    <a href="image1_large.jpg"><img src="image1_thumb.jpg"></a>
    <a href="image2_large.jpg"><img src="image2_thumb.jpg"></a>
</div>
```

### 8. PageRank (GAE-specific)

**Purpose**: Fetch Google PageRank scores for URLs.

**Features**:
- Google Toolbar PageRank checksum algorithm
- Queries Google PageRank API
- Requires Google App Engine

**Usage**:
```python
from PageRank import get_pagerank

# Get PageRank for a URL
pr = get_pagerank('http://example.com')
print(f"PageRank: {pr}")
```

**Note**: Uses deprecated Google API, may not work reliably.

**Key Files**: `PageRank/__init__.py:1`

### 9. urlinfo (GAE-specific)

**Purpose**: Scrape SEO metrics from various search engines.

**Metrics Available**:
- **Google**: Indexed pages, backlinks
- **Baidu**: Pages, links (for Chinese sites)
- **Yahoo**: Pages, inbound links
- **Live/Bing**: Pages, links
- **Social**: Delicious, Reddit, StumbleUpon
- **Validation**: W3C HTML/CSS validators
- **Whois**: Domain information

**URL Patterns**:
```
/urlinfo/gpr/example.com           # Google PageRank
/urlinfo/gpages/example.com        # Google indexed pages
/urlinfo/glinks/example.com        # Google backlinks
/urlinfo/baidupages/example.com    # Baidu pages
/urlinfo/yahoopages/example.com    # Yahoo pages
```

**Key Files**: `urlinfo/__init__.py:1`

### 10. generic_view_patch

**Purpose**: Enhance Django generic views to support extra form fields.

**Problem Solved**: When you need to set model fields that aren't in the form (e.g., `author`, `created_date`).

**Usage**:
```python
from generic_view_patch import create_object, update_object

urlpatterns = [
    url(r'^article/create/$', create_object, {
        'model': Article,
        'form_class': ArticleForm,
        'extra_fields': {
            'author': lambda request, obj: request.user,
            'created_date': lambda request, obj: datetime.now(),
        }
    }),
]
```

**Key Functions**:
- `create_object()`: Enhanced create view
- `update_object()`: Enhanced update view
- `apply_extra_fields_and_save()`: Apply extra fields helper

**Reference**: Based on [Django Snippet #99](http://www.djangosnippets.org/snippets/99/)

**Key Files**: `generic_view_patch/__init__.py:1`

### 11. sitemesh (GAE-specific)

**Purpose**: Template composition with caching for Google App Engine.

**Features**:
- `loadurl` template tag for composable templates
- Memcache integration for performance
- Support for internal and external URLs
- Cache expiration support

**Usage**:
```django
{% load sitemesh %}

<!-- Load and cache external content -->
{% loadurl "http://example.com/widget" 3600 %}

<!-- Load internal view -->
{% loadurl "/internal/sidebar/" %}
```

**Key Files**: `sitemesh/__init__.py:1`

## 🔧 Requirements

- **Django**: 1.0+ (developed for Django 1.0-1.1 era, may need updates for modern Django)
- **Python**: 2.x (uses deprecated syntax, needs migration to Python 3)
- **Google App Engine SDK**: Required for GAE-specific components (PageRank, urlinfo, sitemesh)

### Compatibility Notes

This library was developed circa 2009-2010 and uses:
- Python 2.x syntax (`raise Exception, "message"`)
- Django 1.0-1.1 APIs
- Deprecated Google APIs

**Modernization needed for**:
- Python 3 compatibility
- Current Django versions (3.x/4.x/5.x)
- Alternative APIs for deprecated Google services

## 🎓 Usage Patterns

### Pattern 1: Object Rendering with Lists

```django
{% load render %}

<!-- Render single object -->
{% render article %}

<!-- Render list of objects -->
{% render articles listtemplate="components/article_list.html" %}

<!-- Compact view for sidebar -->
{% render recent_posts templatetype="compact" %}
```

### Pattern 2: Complete Pagination Flow

```django
{% load makeobjectlist paginator render %}

<!-- Create paginated list -->
{% makeobjectlist Article.objects.all paginate_by=15 %}

<!-- Render each article -->
<div class="articles">
    {% for article in object_list %}
        {% render article %}
    {% endfor %}
</div>

<!-- Show pagination controls -->
<div class="pagination">
    {% paginator %}
</div>
```

### Pattern 3: AJAX Partial Updates

```python
# views.py
from renderblock.renderblock import render_block_to_string
from django.http import JsonResponse

def update_comments(request, article_id):
    article = Article.objects.get(id=article_id)
    context = {'article': article, 'comments': article.comments.all()}

    html = render_block_to_string('article_detail.html', 'comments_section', context)

    return JsonResponse({'html': html})
```

```django
<!-- article_detail.html -->
{% block comments_section %}
<div id="comments">
    {% for comment in comments %}
        {% render comment %}
    {% endfor %}
</div>
{% endblock %}
```

### Pattern 4: Custom Template Discovery

```python
# Create template hierarchy:
# templates/
#   components/
#     user.html              # Default
#     user_compact.html      # Compact view
#     user_detailed.html     # Detailed view
#     article.html
#     comment.html
```

```django
{% render user %}                          <!-- uses user.html -->
{% render user templatetype="compact" %}   <!-- uses user_compact.html -->
{% render user templatetype="detailed" %}  <!-- uses user_detailed.html -->
```

## 🐛 Known Issues

1. **Python 2.x Code**: Requires migration to Python 3
2. **Old Django APIs**: May need updates for Django 2.x+
3. **GAE Dependency**: Some components heavily tied to GAE
4. **Eval Usage**: `objectlisttag` uses `eval()` for filters (security concern)
5. **Deprecated APIs**: PageRank uses deprecated Google API
6. **Screen Scraping**: `urlinfo` uses regex scraping (fragile)

## 📖 Development Notes

### Context Management

The template tags use sophisticated context push/pop mechanisms to prevent context pollution during nested renders. See blog post: http://robertmao.com/2010/02/09/contextpushpop/

### Template Tag Argument Parsing

Uses custom `parse_args_kwargs_and_as_var()` helper supporting format:
```django
{% tag arg1 kwarg=value1 kwarg2=value2 as variable_name %}
```

### Recent Development History

- `142044a`: rendertag now supports callable objects
- `ed07f3f`: Improved paginatortag and makeobjectlist tag
- `3f011a0`: Adding objectlisttag (marked unfinished but functional)
- `eb05095`: Adding renderblock functionality
- `de4803d`: Fixed context push/pop issues

## 🤝 Contributing

This is a legacy project that could benefit from:

1. **Python 3 Migration**: Update syntax and APIs
2. **Django Modernization**: Support current Django versions
3. **Security Review**: Remove `eval()` usage, update scraping methods
4. **Test Coverage**: Add comprehensive unit tests
5. **Documentation**: API documentation for each component
6. **GAE Alternatives**: Provide non-GAE versions of utilities

## 📄 License

[Add your license information here]

## 🙏 Acknowledgments

- Original development by Robert Mao
- Based on various Django snippets and community contributions
- Blueprint CSS by Olav Bjørkøy
- jQuery by John Resig and the jQuery team

## 📞 Support

For issues, questions, or contributions, please refer to:
- Project repository: [Add repository URL]
- Developer blog: http://robertmao.com

---

**Note**: This library was developed for Django 1.0-1.1 on Python 2.x and Google App Engine. Modern usage requires updates for Python 3, current Django versions, and alternative APIs for deprecated Google services.
