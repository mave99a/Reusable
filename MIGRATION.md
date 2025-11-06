# Migration Guide: Python 3 & Modern Django

This guide helps you migrate the Django Reusable Components Library from Python 2.x / Django 1.x to Python 3.x and modern Django versions (2.x, 3.x, 4.x, 5.x).

## Table of Contents

- [Overview](#overview)
- [Python 2 to Python 3](#python-2-to-python-3)
- [Django 1.x to Modern Django](#django-1x-to-modern-django)
- [Component-Specific Changes](#component-specific-changes)
- [Testing Migrations](#testing-migrations)
- [Common Issues](#common-issues)

## Overview

### Current State
- **Python**: 2.x syntax
- **Django**: 1.0-1.1 APIs
- **Status**: Functional but outdated

### Migration Goals
- **Python**: 3.8+ compatibility
- **Django**: 3.2+ (LTS) or 4.x/5.x
- **Maintain**: Core functionality
- **Remove**: GAE-specific dependencies (optional)

### Estimated Effort
- **Automatic tools**: ~70% of work
- **Manual fixes**: ~30% of work
- **Testing**: Critical for production use

## Python 2 to Python 3

### Automated Conversion with 2to3

```bash
# Backup first!
cp -r Reusable Reusable.backup

# Run 2to3 on each component
2to3 -w -n rendertag/
2to3 -w -n paginatortag/
2to3 -w -n objectlisttag/
2to3 -w -n renderblock/
2to3 -w -n generic_view_patch/

# For GAE components (optional)
2to3 -w -n PageRank/
2to3 -w -n urlinfo/
2to3 -w -n sitemesh/
```

### Manual Changes Required

#### 1. Exception Syntax

**Before (Python 2)**:
```python
raise Exception, "Template not found"
```

**After (Python 3)**:
```python
raise Exception("Template not found")
```

**Affected Files**:
- `rendertag/templatetags/render.py:85`
- `renderblock/renderblock.py:multiple`

**Find and fix**:
```bash
# Find all raise statements
grep -r "raise.*," . --include="*.py"

# Manual fix required for each
```

#### 2. Iterator Methods

**Before (Python 2)**:
```python
bits.next()
```

**After (Python 3)**:
```python
next(bits)
```

**Affected Files**:
- `rendertag/templatetags/render.py:parse_args_kwargs_and_as_var()`
- Any custom parsing code

**Find and fix**:
```bash
# Find .next() calls
grep -r "\.next()" . --include="*.py"
```

#### 3. String Types

**Before (Python 2)**:
```python
if isinstance(value, basestring):
    # ...
```

**After (Python 3)**:
```python
if isinstance(value, str):
    # ...
```

**Compatibility approach**:
```python
import six  # pip install six

if six.PY2:
    string_types = basestring
else:
    string_types = str

# Use in code
if isinstance(value, string_types):
    # ...
```

#### 4. Dictionary Methods

**Before (Python 2)**:
```python
for key, value in dict.iteritems():
    # ...
```

**After (Python 3)**:
```python
for key, value in dict.items():
    # ...
```

**Note**: 2to3 usually handles this automatically.

#### 5. Print Statements

**Before (Python 2)**:
```python
print "Debug:", value
```

**After (Python 3)**:
```python
print("Debug:", value)
```

**Note**: 2to3 handles this automatically.

#### 6. Import Changes

**Before (Python 2)**:
```python
import urlparse
import urllib2
```

**After (Python 3)**:
```python
from urllib import parse as urlparse
from urllib import request as urllib2
```

**Affected**: `urlinfo/` component (if migrating)

### Compatibility Layer (Six)

For gradual migration supporting both Python 2 and 3:

```python
# requirements.txt
six>=1.16.0

# In code
import six
from six.moves import range
from six.moves.urllib.parse import urlparse

if six.PY2:
    # Python 2 specific code
    string_types = basestring
else:
    # Python 3 specific code
    string_types = str
```

## Django 1.x to Modern Django

### 1. URL Patterns

**Before (Django 1.x)**:
```python
from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('',
    url(r'^articles/$', 'myapp.views.list_articles'),
    url(r'^urlinfo/', include('urlinfo.urls')),
)
```

**After (Django 2.x+)**:
```python
from django.urls import path, include
from myapp import views

urlpatterns = [
    path('articles/', views.list_articles, name='articles_list'),
    path('urlinfo/', include('urlinfo.urls')),

    # Or with regex (re_path)
    # from django.urls import re_path
    # re_path(r'^articles/$', views.list_articles),
]
```

**Affected**: All url configurations

### 2. Template Loading

**Before (Django 1.x)**:
```python
from django.template import Context, Template
from django.template.loader import get_template

t = get_template('template.html')
html = t.render(Context({'var': value}))
```

**After (Django 2.x+)**:
```python
from django.template.loader import get_template

t = get_template('template.html')
html = t.render({'var': value})  # Dict, not Context
```

**Affected**: `renderblock/renderblock.py`

### 3. Context Processors

**Before (Django 1.x)**:
```python
from django.template import RequestContext

def my_view(request):
    return render_to_response('template.html',
                            {'var': value},
                            context_instance=RequestContext(request))
```

**After (Django 2.x+)**:
```python
from django.shortcuts import render

def my_view(request):
    return render(request, 'template.html', {'var': value})
```

**Note**: The `render()` shortcut automatically uses RequestContext.

### 4. Pagination API

**Current code should work**, but verify:

```python
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# This API is stable across versions
paginator = Paginator(object_list, 10)
page_obj = paginator.get_page(page_number)  # Django 2.0+
```

**Note**: `get_page()` is preferred over `page()` in Django 2.0+

### 5. Template Tag Registration

**Before (Django 1.x)**:
```python
from django import template
register = template.Library()

@register.tag(name='render')
def do_render(parser, token):
    # ...
```

**After (Django 2.x+)**:
```python
# Same syntax still works!
from django import template
register = template.Library()

@register.tag(name='render')
def do_render(parser, token):
    # ...
```

**Note**: Template tag API is largely unchanged.

### 6. Settings Configuration

**Update settings.py for modern Django**:

```python
# settings.py for Django 3.2+

# TEMPLATES setting (replaces old TEMPLATE_* settings)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Django 3.1+ Path support
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Use pathlib for paths (Django 3.1+)
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

# STATIC and MEDIA
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### 7. Import Path Changes

**Django 1.x to 2.x+**:

```python
# Old
from django.core.urlresolvers import reverse
from django.conf.urls import url, include

# New
from django.urls import reverse
from django.urls import path, re_path, include
```

## Component-Specific Changes

### rendertag

**File**: `rendertag/templatetags/render.py`

**Changes needed**:

1. Fix exception syntax:
```python
# Line ~85
# Before
raise Exception, "err: template %s not found. object type: %s" % (template_name, type(obj))

# After
raise Exception("err: template %s not found. object type: %s" % (template_name, type(obj)))
```

2. Fix iterator:
```python
# In parse_args_kwargs_and_as_var()
# Before
token = bits.next()

# After
token = next(bits)
```

3. Update template rendering:
```python
# Before
return template.render(Context(context))

# After
return template.render(context)
```

**Modernized version**:
```python
import logging
from django import template
from django.template.loader import get_template
from django.template import TemplateDoesNotExist

register = template.Library()

class RenderNode(template.Node):
    def __init__(self, obj, template=None, listtemplate=None, templatetype=None):
        self.obj = obj
        self.template = template
        self.listtemplate = listtemplate
        self.templatetype = templatetype

    def render(self, context):
        obj = self.obj.resolve(context)

        # Handle None
        if obj is None:
            return ''

        # Handle callable
        if callable(obj):
            obj = obj()

        # Determine template
        template_name = self._get_template_name(obj)

        try:
            tmpl = get_template(template_name)
            # Django 2.x+ accepts dict directly
            render_context = {'object': obj}
            render_context.update(context.flatten())
            return tmpl.render(render_context)
        except TemplateDoesNotExist:
            logging.error(f"Template not found: {template_name}")
            return f"[err: template {template_name} not found]"

    def _get_template_name(self, obj):
        if self.template:
            return self.template

        class_name = obj.__class__.__name__.lower()
        if self.templatetype:
            return f"components/{class_name}_{self.templatetype}.html"
        return f"components/{class_name}.html"

@register.tag(name='render')
def do_render(parser, token):
    bits = iter(token.split_contents())
    next(bits)  # Skip tag name

    # Parse arguments
    obj = parser.compile_filter(next(bits))
    template = None
    listtemplate = None
    templatetype = None

    for bit in bits:
        if '=' in bit:
            name, value = bit.split('=', 1)
            value = value.strip('\'"')
            if name == 'template':
                template = value
            elif name == 'listtemplate':
                listtemplate = value
            elif name == 'templatetype':
                templatetype = value

    return RenderNode(obj, template, listtemplate, templatetype)
```

### paginatortag

**File**: `paginatortag/templatetags/paginator.py`

**Changes needed**:
- Minimal changes required
- Verify Paginator API usage
- Update any string type checks

### objectlisttag

**File**: `objectlisttag/templatetags/makeobjectlist.py`

**Changes needed**:

1. **Security**: Replace eval() with safer alternatives:

```python
# Before (UNSAFE)
if addition_filter:
    object_list = eval('object_list' + addition_filter)

# After (SAFER - but still validate input!)
if addition_filter:
    # Only allow simple filter chains
    if not re.match(r'^(\.\w+\([^)]*\))+$', addition_filter):
        raise ValueError("Invalid filter format")
    # Use exec with restricted namespace
    namespace = {'object_list': object_list}
    exec(f'result = object_list{addition_filter}', namespace)
    object_list = namespace['result']

# Even better: Use Q objects
from django.db.models import Q

# Accept filter kwargs instead
# {% makeobjectlist articles published=True category="tech" paginate_by=10 %}
```

2. Update exception handling:
```python
# Modern Django
try:
    page_obj = paginator.page(page)
except (EmptyPage, PageNotAnInteger):
    page_obj = paginator.page(1)
```

### renderblock

**File**: `renderblock/renderblock.py`

**Changes needed**:

1. Context usage:
```python
# Before
from django.template import Context
c = Context(context)

# After
c = context  # Already a dict
```

2. Template rendering:
```python
# Before
return template.render(Context(context))

# After
return template.render(context)
```

### generic_view_patch

**File**: `generic_view_patch/__init__.py`

**Status**: **Deprecated - Use Class-Based Views instead**

**Modern Alternative**:
```python
# Instead of patching generic views, use CBVs
from django.views.generic import CreateView, UpdateView

class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm

    def form_valid(self, form):
        # Set extra fields
        form.instance.author = self.request.user
        form.instance.created_date = timezone.now()
        return super().form_valid(form)

# urls.py
path('article/create/', ArticleCreateView.as_view(), name='article_create')
```

### GAE Components (PageRank, urlinfo, sitemesh)

**Status**: **Requires major rewrite or replacement**

**Options**:

1. **Replace with modern alternatives**:
   - PageRank: Use SEO APIs (Moz, Ahrefs, SEMrush)
   - urlinfo: Use requests library + BeautifulSoup
   - sitemesh: Use Django's cache framework

2. **Remove if not needed**:
```python
# Don't include in INSTALLED_APPS
# Remove from requirements
```

## Testing Migrations

### 1. Create Virtual Environment

```bash
# Python 3.8+
python3 -m venv venv-py3
source venv-py3/bin/activate

# Install Django
pip install django==3.2  # or 4.2, 5.0
```

### 2. Test Each Component

```python
# test_rendertag.py
import unittest
from django.test import TestCase
from django.template import Template, Context

class RenderTagTestCase(TestCase):
    def test_basic_render(self):
        template = Template('{% load render %}{% render obj %}')
        # ... test cases
```

### 3. Run Tests

```bash
# Create test project
django-admin startproject testproject
cd testproject

# Copy components
cp -r ../Reusable/rendertag .

# Add to INSTALLED_APPS and run tests
python manage.py test rendertag
```

### 4. Manual Testing

```bash
# Start development server
python manage.py runserver

# Test each feature:
# - Object rendering
# - Pagination
# - CSS/JS loading
# - etc.
```

## Common Issues

### Issue: Template.render() takes 1 argument

**Error**: `TypeError: render() takes 1 positional argument but 2 were given`

**Cause**: Django 1.x used `Context`, Django 2.x+ uses dict

**Fix**:
```python
# Remove Context wrapper
# Before
template.render(Context(context_dict))

# After
template.render(context_dict)
```

### Issue: No module named django.conf.urls.defaults

**Error**: `ImportError: No module named django.conf.urls.defaults`

**Cause**: Module removed in Django 2.0

**Fix**:
```python
# Before
from django.conf.urls.defaults import patterns, url

# After
from django.urls import path, re_path
```

### Issue: render_to_response not available

**Error**: `ImportError: cannot import name 'render_to_response'`

**Cause**: Removed in Django 3.0

**Fix**:
```python
# Before
from django.shortcuts import render_to_response

# After
from django.shortcuts import render
```

### Issue: context_instance deprecated

**Warning**: `RemovedInDjango110Warning: context_instance is deprecated`

**Fix**: Use `render()` shortcut instead of `render_to_response()`

## Migration Checklist

- [ ] Run 2to3 on all Python files
- [ ] Fix exception syntax (`raise X, Y` → `raise X(Y)`)
- [ ] Fix iterator calls (`.next()` → `next()`)
- [ ] Update URL patterns (patterns → list)
- [ ] Update template rendering (remove Context wrapper)
- [ ] Replace eval() in objectlisttag
- [ ] Update imports (urlresolvers → urls)
- [ ] Test all template tags
- [ ] Test pagination
- [ ] Test media file serving
- [ ] Update documentation
- [ ] Run full test suite
- [ ] Deploy to staging environment
- [ ] User acceptance testing

## Recommended Migration Path

1. **Phase 1**: Python 3 compatibility
   - Run automated tools
   - Fix syntax errors
   - Test basic functionality

2. **Phase 2**: Django 2.2 LTS
   - Update to Django 2.2 (last Python 2 compatible)
   - Fix deprecation warnings
   - Update URL patterns

3. **Phase 3**: Django 3.2 LTS
   - Ensure Python 3 only
   - Update all deprecated APIs
   - Full regression testing

4. **Phase 4**: Django 4.2 LTS (Current)
   - Optional: migrate to modern patterns
   - Replace function-based with class-based views
   - Use modern async features if needed

## Resources

- [Django 2.0 Release Notes](https://docs.djangoproject.com/en/2.0/releases/2.0/)
- [Django 3.0 Release Notes](https://docs.djangoproject.com/en/3.0/releases/3.0/)
- [Django 4.0 Release Notes](https://docs.djangoproject.com/en/4.0/releases/4.0/)
- [Python 2to3 Tool](https://docs.python.org/3/library/2to3.html)
- [Six: Python 2 and 3 Compatibility](https://six.readthedocs.io/)

---

Last updated: 2025-11-06
