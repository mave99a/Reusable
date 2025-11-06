# URL Intelligence Services

## Overview
`urlinfo` exposes a collection of lightweight HTTP endpoints that return
metadata about a given domain. The views proxy various third-party services
(Google, Bing, Baidu, Yahoo, Delicious, Reddit, StumbleUpon, W3C validators,
ShareThis, etc.) through Google App Engine's `urlfetch` API and normalise the
responses to plain text.

## Available endpoints
Each endpoint accepts a URL or hostname (depending on the upstream service) and
returns the scraped metric as the response body.

* `/gpr/<site>/` – Google Toolbar PageRank.
* `/gpages/<site>/`, `/glinks/<site>/` – Google indexed pages and backlinks.
* `/livepages/<site>/`, `/livelinks/<site>/` – Bing indexed pages and backlinks.
* `/baidupages/<site>/`, `/baidulinks/<site>/` – Baidu indexed pages and backlinks.
* `/ypages/<site>/`, `/ylinks/<site>/` – Yahoo site explorer counts.
* `/delicious/<site>/`, `/reddit/<site>/`, `/stumbleupon/<site>/` – social bookmarking counts.
* `/w3chtml/<site>/`, `/w3ccss/<site>/` – W3C validation status messages.
* `/whois/<site>/` – Domain owner (via trynt.com WHOIS API).

All endpoints are wired up in `urls.py` for quick inclusion in a project.

## Usage
Include the URLs in your project and proxy the responses as needed:

```python
from django.conf.urls.defaults import include, patterns

urlpatterns = patterns('',
    (r'^urlinfo/', include('urlinfo.urls')),
)
```

Consider caching results aggressively, as each call hits a remote service and
may be rate limited.
