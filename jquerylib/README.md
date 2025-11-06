# jQuery Library Bundle

## Overview
`jquerylib` collects a set of jQuery core and plugin scripts and registers them
with Ragendja's media pipeline. Importing `jquerylib.settings` ensures the files
are concatenated into a single combined JavaScript asset.

## Included scripts
* `jquery.js` – core jQuery runtime.
* `jquery.fixes.js` – project specific fixes.
* `jquery.ajax-queue.js`
* `jquery.bgiframe.js`
* `jquery.livequery.js`
* `jquery.form.js`

All scripts live in the `media/` directory for use with Django's static file
serving.

## Installation
1. Add `jquerylib` to `INSTALLED_APPS`.
2. Import `jquerylib.settings` from your project settings so Ragendja can add
the bundle to `combined-<language>.js`.

## Usage
After installation you can include the combined asset in templates:

```html
<script src="{% static 'combined-en.js' %}"></script>
```

If you prefer the individual files, point to `/media/jquerylib/` based on your
static configuration.
