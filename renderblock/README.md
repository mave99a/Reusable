# Render Block Helper

## Overview
`renderblock` exposes utilities for rendering a specific template block without
rendering an entire template to the browser. It is useful for AJAX endpoints or
composing HTML snippets that reuse blocks defined in base templates.

## Highlights
* `render_template_block()` – render a block from a previously rendered template
  instance.
* `render_block_to_string()` – load a template by name and return the rendered
  block as a string.
* `direct_block_to_template()` – view helper that responds with a block rendered
  from a template, accepting optional extra context.

## Usage example
```python
from renderblock.renderblock import direct_block_to_template


def modal_fragment(request):
    return direct_block_to_template(
        request,
        template='articles/detail.html',
        block='modal_content',
        extra_context={'article_id': request.GET.get('id')}
    )
```

If the block cannot be located a `BlockNotFound` exception is raised.
