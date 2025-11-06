# Generic View Patch

## Overview
`generic_view_patch` provides drop-in replacements for Django's legacy
`django.views.generic.create_update` helpers. The patched versions add support
for supplying `extra_fields` that are injected into the model instance before it
is saved.

## Key features
* Works as a transparent replacement for `create_object` and `update_object`.
* Accepts a callable or dict of `extra_fields` and applies them before saving.
* Respects authentication checks (`login_required`) and custom templates just
  like the original generic views.

## Installation
1. Place `generic_view_patch` on your Python path and add it to
   `INSTALLED_APPS` if you want to ship it as an app.
2. Import `create_object` / `update_object` from this package instead of the
   deprecated Django module:

```python
from generic_view_patch.create_update import create_object, update_object
```

## Usage
Pass an `extra_fields` dictionary or callable when invoking the view helper:

```python
def create_article(request):
    return create_object(
        request,
        model=Article,
        extra_fields=lambda req: {'author': req.user},
        post_save_redirect='article_detail'
    )
```

The callable receives the current request and can return a dictionary that will
be applied to the model instance before saving.
