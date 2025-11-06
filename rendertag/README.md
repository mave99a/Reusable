# Render Template Tag

## Overview
`rendertag` introduces a versatile `{% render %}` template tag that can render a
single object, a list of objects, or the result of a callable into HTML. It is
designed for reusable components that map objects to template fragments stored
under a shared `components/` directory.

## Features
* Auto-selects a template based on the object's class name (e.g.
  `components/article.html`).
* Supports `template`, `templatetype`, and `listtemplate` keyword arguments to
  override the template path or how lists are rendered.
* Can execute callables referenced by dotted import path and render or assign
  their return value.

## Usage examples
```django
{% load render %}

{# Render a single object using the default template naming convention #}
{% render article %}

{# Render using an explicit template #}
{% render article template='components/article_card.html' %}

{# Render a list of objects with a custom list template #}
{% render article_list listtemplate='components/article_list.html' %}
```

When rendering lists, the tag will automatically wrap the output in either a
`<ul>` or `<table>` depending on the first rendered item unless a `listtemplate`
is supplied.
