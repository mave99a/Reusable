# SiteMesh-inspired Content Loader

## Overview
The `sitemesh` app delivers a `{% loadurl %}` template tag that can fetch and
cache external or internal URLs, injecting the fetched markup into the current
page. It is inspired by SiteMesh-style page decoration and uses Google App
Engine's `urlfetch` and `memcache` services.

## Features
* Fetches HTTP content from remote URLs.
* Resolves internal Django URLs via `django.core.urlresolvers.resolve`.
* Caches responses in App Engine memcache with a configurable expiry time.

## Usage
```django
{% load sitemesh %}
{% loadurl 'https://example.com/sidebar/' 3600 %}
```

The second argument is an optional cache expiration (in seconds). When pointing
at an internal URL the tag will call the underlying view with the current
`request` if available in the template context.
