# Sexy Lightbox Assets

## Overview
The `lightbox` package ships the Sexy Lightbox v2.3 assets (stylesheets and
scripts) and registers them with Ragendja so they can participate in the
combined media pipeline for Google App Engine Django projects.

## Contents
* `media/sexylightbox.css`
* `media/sexylightbox.v2.3.jquery.js`
* `media/jquery.easing.1.3.js`
* `settings.py` – registers both CSS and JavaScript bundles with Ragendja.

## Installation
1. Add `lightbox` to `INSTALLED_APPS`.
2. Import `lightbox.settings` during startup (e.g. from your project settings).

## Usage
Include the combined assets inside your templates:

```html
<link rel="stylesheet" href="{% static 'combined-en.css' %}">
<script src="{% static 'combined-en.js' %}"></script>
```

Once loaded you can initialize Sexy Lightbox according to the plugin
instructions, e.g.:

```javascript
$(function () {
  SexyLightbox.config.overlayColor = '#000';
  SexyLightbox.initialize();
});
```
