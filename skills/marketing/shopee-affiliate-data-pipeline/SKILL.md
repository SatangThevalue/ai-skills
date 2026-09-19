---
name: shopee-affiliate-data-pipeline
description: "Fetch and score Shopee affiliate products using pricing and seasonal matrices."
version: 0.1.0
metadata:
  hermes:
    tags: [Shopee, Affiliate, Scraping, Data-Pipeline, Monetization]
    related_skills: [zero-touch-monetization-playbook, thailand-market-demand-2026-2027]
---

# Shopee Affiliate Data Pipeline

This skill defines the data extraction and scoring logic for sourcing "Winning Products" from Shopee for Affiliate Marketing. It acts as the upstream data source for the Zero-Touch Monetization engine, filtering out low-margin or hard-to-sell items before passing them to the AI Script Generator.

## When to Use
- Fetching daily product ideas for TikTok/Facebook Reels automation.
- Evaluating if a product meets the 2026-2027 Thai consumer economic constraints.
- Automating affiliate link generation.

## Prerequisites
- Python environment with `requests` and `beautifulsoup4` (if scraping fallback is used).
- Shopee Open API Credentials (App ID, App Secret) OR Playwright for headless scraping.

## How to Run
Invoke the extraction logic via the `terminal` tool using a Python script, and store the resulting JSON into the PostgreSQL `trading_data` database.

## Quick Reference
- **Winning Formula:** (Price 199-499 THB) + (Comm > 10%) + (Visual Before/After) + (Seasonal Match)
- **Target Endpoint (API):** `https://partnerapi.shopeemobile.com/api/v2/affiliate/...`

## Procedure

1. **Implement the Scoring Matrix (Python)**
   Create a script `scripts/shopee_scorer.py` that evaluates products.

   ```python
   def calculate_winning_score(price: float, commission_rate: float, category: str, current_month: int) -> int:
       score = 0
       
       # 1. Price Dimension (Impulse Buy: 199 - 499 THB)
       if 199 <= price <= 499:
           score += 10
       elif price < 199:
           score += 7
       else:
           score += 2
           
       # 2. Commission Dimension (> 10%)
       if commission_rate >= 10.0:
           score += 10
       elif commission_rate >= 5.0:
           score += 5
           
       # 3. Visual Dimension (Home/Living, Gadgets)
       visual_categories = ["Home & Living", "Mobile Gadgets", "Automotive Care"]
       if category in visual_categories:
           score += 10
           
       # 4. Seasonal Dimension (e.g., Q2 Summer/Rainy)
       rainy_items = ["Umbrella", "Waterproof", "Raincoat", "Mosquito"]
       # Add logic to check keywords against current_month
       
       return score
   ```

2. **Fetch Data (Mock / API structure)**
   ```python
   import requests

   def get_top_affiliate_products(api_key):
       # Placeholder for actual Shopee API call
       # Normally requires signed requests using HMAC-SHA256
       sample_data = [
           {"id": 101, "name": "ไม้ถูพื้นรีดน้ำอัตโนมัติ", "price": 299, "comm_rate": 15.0, "category": "Home & Living"},
           {"id": 102, "name": "ตู้เย็น 2 ประตู", "price": 5990, "comm_rate": 2.0, "category": "Home Appliances"}
       ]
       
       winning_products = []
       for p in sample_data:
           score = calculate_winning_score(p['price'], p['comm_rate'], p['category'], 9)
           if score >= 25: # Threshold
               winning_products.append(p)
               
       return winning_products
   ```

## Pitfalls
- **API Rate Limits & Authentication:** Shopee Open API requires strict timestamp and signature calculation. If signatures mismatch, you get 401 Unauthorized.
- **Dynamic Links:** Affiliate links expire or change. Always generate the short link at runtime before posting.
- **Stock Depletion:** A product might have a high score but 0 stock. Always filter `stock > 50` to avoid driving traffic to dead pages.

## Verification
Run the python script to output a list of scored products. Ensure no product over 1,000 THB passes the "Winning Product" threshold unless commission is exceptionally high.