# PageRank Utility

## Overview
This package exposes a small helper that queries the (now legacy) Google Toolbar
PageRank API. It implements the checksum algorithm locally and issues the
request using `google.appengine.api.urlfetch` so it can be executed inside a
Google App Engine project.

## Provided functionality
* `PageRank.PageRank(url)`: returns an integer PageRank score for the given URL.

## Dependencies
* Google App Engine runtime (for `urlfetch`).
* Python standard library only.

## Usage
```python
from PageRank import PageRank

score = PageRank('https://www.djangoproject.com/')
print('Toolbar PageRank:', score)
```

The helper is synchronous and will return `0` if the remote service cannot be
reached or an unexpected payload is returned.

## Notes
The Toolbar PageRank API is deprecated and may stop responding at any time.
Consider providing graceful fallbacks in production code.
