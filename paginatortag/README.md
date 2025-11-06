# Paginator Template Tag

## Overview
The `paginatortag` app provides an inclusion tag that renders Digg-style
pagination controls using the `paginator` and `page_obj` context variables.
Pair it with `objectlisttag` or any other view that exposes these variables.

## Components
* `templatetags/paginator.py` – defines the inclusion tag that prepares context
  data for the template.
* `templates/paginator.html` – default markup for the pagination controls.

## Usage
1. Ensure your view or preceding template code adds `page_obj` and `paginator`
   to the context (for example via `{% makeobjectlist %}`).
2. Load the tag library and render the inclusion tag:

```django
{% load paginator %}
{% paginator %}
```

The context dictionary contains helper values such as `page_numbers`,
`has_previous`, and `has_next`, allowing you to customize the `paginator.html`
template if needed.
