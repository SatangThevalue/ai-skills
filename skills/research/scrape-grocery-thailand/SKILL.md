---
name: scrape-grocery-thailand
description: "Use when scraping, crawling, or extracting grocery product information from Thai retailers (specifically Lotus's and Makro Pro) via Python scripts."
version: 1.0.0
author: Tonthong
license: MIT
metadata:
  hermes:
    tags: [web-scraping, grocery, api-crawling, th-retail, comparison]
    related_skills: [research-to-skill-pipeline, software-development:hermes-agent-skill-authoring]
---

# Scrape Grocery Thailand (Lotus's, Makro Pro & Big C Online)

## Overview
This skill outlines how to programmatically extract product information (names, prices, SKUs, images, stock, etc.) from **Lotus's Thailand**, **Makro Pro**, and **Big C Online** websites using direct, unauthenticated backend APIs. Utilizing internal JSON/GraphQL API requests is significantly faster, more reliable, and lighter on tokens than UI rendering via Selenium/Playwright, bypassing typical anti-scraping and CAPTCHA bottlenecks.

## When to Use
- Building price-matching, SKU-matching, or market analysis scripts.
- Extracting raw product data, sizes, quantities, and pricing updates.
- Implementing periodic web monitors/watchdogs for grocery item changes.

---

## 1. Lotus's Thailand API Guide

### Endpoint
Lotus's uses a backend API-BFF (Backend-For-Frontend) endpoint:
- **Base Search URL:** `https://api-o2o.lotuss.com/lotuss-mobile-bff/product/v5/search`
- **Method:** `POST`
- **Headers:** 
  - `Content-Type: application/json`
  - `Accept: application/json`
  - `Accept-Language: th` or `en`
  - `User-Agent` (standard browser agent string)

### POST Body Parameters
```json
{
  "keyword": "น้ำดื่ม",
  "limit": 15,
  "page": 1,
  "seller_id": 3
}
```

### Python Implementation Example
```python
import urllib.request
import urllib.parse
import json
import ssl

def search_lotus(keyword, limit=15, page=1):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    url = "https://api-o2o.lotuss.com/lotuss-mobile-bff/product/v5/search?sort=relevance:DESC&limit=15&page=1&seller_id=3"
    body = {
        "keyword": keyword,
        "limit": limit,
        "page": page,
        "seller_id": 3
    }
    
    req = urllib.request.Request(
        url,
        method="POST",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Accept-Language": "th"
        }
    )
    
    with urllib.request.urlopen(req, context=ctx) as r:
        response_data = json.loads(r.read().decode("utf-8"))
        return response_data.get("data", {}).get("products", [])
```

### Key Output Fields (Lotus's)
- `name`: Product title (e.g. `คริสตัล น้ำดื่ม 1500 มล. แพ็ค 6`)
- `sku`: Unique SKU identifier (e.g. `164935888`)
- `finalPricePerUOW`: Final sale price
- `regularPricePerUOW`: Normal price before discounts
- `thumbnail.url`: Direct link to product image
- `stockStatus`: Product availability (`IN_STOCK`, `OUT_OF_STOCK`)

---

## 2. Makro Pro Search API Guide

### Endpoint
Makro Pro utilizes a custom search index service (Maknet):
- **Base Search URL:** `https://search.maknet.siammakro.cloud/search/api/v1/indexes/products/search`
- **Method:** `POST`
- **Headers:**
  - `Content-Type: application/json`
  - `Accept: application/json`
  - `User-Agent` (standard browser agent string)

### POST Body Parameters
```json
{
  "q": "น้ำดื่ม",
  "limit": 10
}
```

### Python Implementation Example
```python
import urllib.request
import json
import ssl

def search_makro(query, limit=10):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    url = "https://search.maknet.siammakro.cloud/search/api/v1/indexes/products/search"
    body = {
        "q": query,
        "limit": limit
    }
    
    req = urllib.request.Request(
        url,
        method="POST",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    )
    
    with urllib.request.urlopen(req, context=ctx) as r:
        response_data = json.loads(r.read().decode("utf-8"))
        hits = response_data.get("hits", [])
        products = [h.get("document", {}) for h in hits]
        return products
```

### Key Output Fields (Makro Pro)
- `title` / `searchTitle.TH`: Product title (e.g. `น้ำทิพย์ น้ำดื่ม 550 มล. x 12`)
- `sku`: Product SKU code
- `displayPrice`: Current sale price
- `originalPrice`: Regular price
- `soldCount`: Total units sold historical value
- `images`: Array of product image URLs
- `inStock`: Inventory status (`1` for in stock, `0` for out)
- `brand` / `brandEn`: Product brand

---

## 3. Big C Online Search API Guide

### Endpoint
Big C Online uses Next.js server-side rendering (SSR) data endpoints. To query products, the script must first fetch Big C's homepage to extract the current active Next.js `buildId`, then call the JSON data endpoints.
- **Home URL (to extract buildId):** `https://www.bigc.co.th/`
- **Base Search URL:** `https://www.bigc.co.th/_next/data/{buildId}/search.json`
- **Base Category URL:** `https://www.bigc.co.th/_next/data/{buildId}/category/{category_slug}.json`
- **Method:** `GET`
- **Query Parameters:**
  - Search: `q` (keyword), `page` (optional, default 1)
  - Category: `slug` (category_slug), `page` (optional, default 1)
- **Headers:**
  - `User-Agent` (standard browser agent string)
  - `Accept: application/json`

### Python Implementation Example
```python
import urllib.request
import urllib.parse
import json
import re
import ssl

def get_bigc_build_id():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    url = "https://www.bigc.co.th/"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    )
    with urllib.request.urlopen(req, context=ctx) as r:
        html = r.read().decode("utf-8")
        match = re.search(r'\"buildId\":\"([^\"]+)\"', html)
        if match:
            return match.group(1)
    raise ValueError("Big C Next.js buildId not found")

def search_bigc(keyword, page=1):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    build_id = get_bigc_build_id()
    quoted_keyword = urllib.parse.quote(keyword)
    url = f"https://www.bigc.co.th/_next/data/{build_id}/search.json?q={quoted_keyword}&page={page}"
    
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json"
        }
    )
    with urllib.request.urlopen(req, context=ctx) as r:
        data = json.loads(r.read().decode("utf-8"))
        products_summary = data.get("pageProps", {}).get("productCategory", {}).get("products_summary", {})
        return products_summary.get("products", [])
```

### Key Output Fields (Big C)
- `name`: Product title (e.g. `น้ำทิพย์ น้ำดื่ม 550 มล. 12 ขวด`)
- `sku`: Product SKU (usually EAN-13 barcode like `8851959439715`)
- `price_sales`: Current selling price (including discounts)
- `price_base` / `price_incl_tax`: Regular price before promotion
- `thumbnail_image`: URL to product image
- `stock`: Inventory availability status (`Y` for yes, `N` for no)
- `slug`: Product slug for direct URL generation (`https://www.bigc.co.th/product/{slug}`)

---

## 4. Data Extraction Regex & Preprocessing
Grocery comparison tasks require extracting clean numerical metric volumes and package counts from product title string patterns:

### Volume & Unit Regex
Standardizes volumes into milliliters (mL) or grams (g):
```python
# Regex to match 1500 มล, 1.5 ลิตร, 550 ml, etc.
pattern = r'(\d+(?:\.\d+)?)\s*(มล|ก\.|กรัม|ลิตร|ล|ml|l|g)'
```

### Quantity (Pack Count) Regex
Parses multi-pack listings (e.g. "แพ็ค 6", "x 12", "15 unit(s)"):
```python
# Regex to match pack details or x12 / X 6
pack_pattern = r'แพ็ค\s*(\d+)|[xX]\s*(\d+)|(\d+)\s*unit\(s\)'
```

## Common Pitfalls
1. **SSLError / Timeout Exceptions:** Ensure `ssl._create_unverified_context()` or `ssl.CERT_NONE` context is used if the server certificate validation fails from isolated environments.
2. **Missing `User-Agent` Headers:** Retail APIs will block python's default user-agent with `403 Forbidden` or `400 Bad Request`.
3. **Product Slug / ID Shifts:** Lotus's page parameters can be dynamically generated. Always use the search endpoints (`/v5/search`) rather than browsing directly when querying programmatically.
4. **Dynamic Build ID on Big C:** Big C uses Next.js dynamic routing. Directly calling a hardcoded `buildId` route will fail with a `404` or `307` redirect if the site has redeployed. Always parse the active `buildId` from the homepage first.
5. **Cloudflare Protection on Big C:** Big C Online uses Cloudflare verification which blocks simple HTTP requests (like python's default `urllib` or standard `requests` without browser fingerprinting). When scraping Big C, you must either:
   - Use browser automation tools like Playwright or Selenium that execute Javascript and handle Cloudflare cookies.
   - Use specialized HTTP clients like `curl_cffi` (impersonating a browser fingerprint) or pass valid `__cf_bm` cookies and User-Agent headers extracted from an active session.

## Verification Checklist
- [ ] Perform a test POST query against Lotus's BFF Endpoint using `keyword`.
- [ ] Perform a test POST query against Makro's Search Endpoint using `q`.
- [ ] Perform a test GET query against Big C's Next.js endpoints using dynamic `buildId`.
- [ ] Confirm product keys contain `finalPricePerUOW` (Lotus's), `displayPrice` (Makro Pro), and `price_sales` (Big C Online).
