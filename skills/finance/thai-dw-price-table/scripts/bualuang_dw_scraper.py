import urllib.request
from bs4 import BeautifulSoup

def scrape_bualuang_dw_table(dw_symbol):
    """
    Scrape DW01 (Bualuang) price table using BeautifulSoup.
    Target URL: https://www.blswarrant.com/mydw/{dw_symbol}
    Returns a list of data rows, or None if failed.
    """
    url = f"https://www.blswarrant.com/mydw/{dw_symbol}"
    print(f"Fetching: {url}")
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as res:
            html = res.read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            tables = soup.find_all('table')
            
            if len(tables) > 1:
                # Table [1] is the "ราคาเสนอซื้อคืนเบื้องต้น" table
                price_table = tables[1]
                rows = price_table.find_all('tr')
                
                data = []
                # Skip first row (Title) and extract from row index 1 onwards
                for row in rows[1:]: 
                    cols = row.find_all(['th', 'td'])
                    clean_cols = [c.text.strip().replace('\n', '') for c in cols if c.text.strip() != '']
                    if clean_cols:
                        data.append(clean_cols)
                        
                return data
            else:
                print(f"Table not found for {dw_symbol}")
                return None
    except Exception as e:
        print(f"Error fetching DW01 for {dw_symbol}: {e}")
        return None

if __name__ == '__main__':
    # Test
    res = scrape_bualuang_dw_table('SET5001C2607A')
    if res:
        print("Scrape successful. First 5 rows:")
        for r in res[:5]:
            print(r)
