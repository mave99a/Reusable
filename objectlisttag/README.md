# Object List Template Tag

## Overview
`objectlisttag` provides a `{% makeobjectlist %}` template tag that simplifies
building paginated object lists in templates. It works together with Django's
`Paginator` and exposes the paginated data through context variables that can be
consumed by additional components (e.g., the paginator tag found in this
repository).

## Features
* Resolve an object or queryset from the template context.
* Optionally invoke a chained attribute or manager method via
  `addtion_filter` (e.g. `"comments.all"`).
* Adds the paginated results to the context under a configurable variable name.

## Usage
Load the tag library and render a paginated list:

```django
{% load makeobjectlist %}
{% makeobjectlist article_list paginate_by=20 as articles %}

<ul>
  {% for article in articles %}
    <li>{{ article.title }}</li>
  {% endfor %}
</ul>
```

The tag also injects `paginator` and `page_obj` into the context so you can use
pagination controls from `paginatortag`.
