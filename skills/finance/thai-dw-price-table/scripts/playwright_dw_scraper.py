"""
Example of using Playwright to scrape DW price tables from Client-Side Rendered (React/Vue) websites like DW28 (Macquarie) or DW41 (JPMorgan).

Prerequisites:
  pip install playwright
  playwright install chromium
"""
from playwright.sync_api import sync_playwright

def scrape_dw_with_playwright(url, dw_symbol):
    """
    Spawns a headless browser to wait for the JavaScript rendering to complete.
    """
    print(f"Opening headless browser for {dw_symbol}...")
    with sync_playwright() as p:
        # Launch Chromium headless
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to the target page
        page.goto(url)
        
        try:
            # Wait for the table element to appear in the DOM (timeout 10s)
            page.wait_for_selector("table", timeout=10000)
            
            # Extract the fully rendered HTML
            html = page.content()
            
            # Here you would pass 'html' to BeautifulSoup to extract the table data
            # ...
            print(f"Successfully loaded {len(html)} bytes of rendered HTML.")
            
        except Exception as e:
            print(f"Timeout or error while waiting for table: {e}")
            
        finally:
            browser.close()

if __name__ == '__main__':
    # Example for DW28
    scrape_dw_with_playwright("https://www.thaidw.com/tools/livematrix/SET5028C2405A", "SET5028C2405A")
