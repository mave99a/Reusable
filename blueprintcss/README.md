# Blueprint CSS Media Bundle

## Overview
This package bundles the Blueprint CSS assets for use inside a Ragendja / Google
App Engine powered Django project. The included `settings.py` helper registers
the Blueprint stylesheets with Ragendja's `settings_post` integration so they
are collected into the combined asset pipeline.

## Contents
* `media/` – upstream Blueprint CSS files (`screen.css`, `print.css`, `ie.css`).
* `settings.py` – hooks that register the assets with Ragendja.

## Installation
1. Add `blueprintcss` to your `INSTALLED_APPS`.
2. Import `blueprintcss.settings` somewhere during startup (e.g. inside your
   project settings module) so Ragendja knows about the static files.

## Usage
Once installed you can reference the combined stylesheet in your templates:

```html
<link rel="stylesheet" href="{% static 'combined-en.css' %}">
```

To use the uncombined assets directly, reference files in
`/media/blueprintcss/` based on your static files configuration.
