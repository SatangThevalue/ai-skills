import urllib.request
import re
from bs4 import BeautifulSoup

def scrape_kgi_dw_table(dw_symbol):
    """
    Scrape DW13 (KGI) price table using BeautifulSoup.
    Target URL: https://www.thaiwarrant.com/dw/{dw_symbol}
    Returns a dictionary with dates and data rows, or None if failed.
    """
    url = f'https://www.thaiwarrant.com/dw/{dw_symbol}'
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as res:
            html = res.read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            
            tables = soup.find_all('table')
            if len(tables) > 1:
                price_table = tables[1]
                rows = price_table.find_all('tr')
                
                # Extract header dates (Row 2, skip first col)
                header_row = rows[1].find_all(['th', 'td'])
                dates = [c.text.strip() for c in header_row[1:]]
                
                data = []
                # Extract price data (skip first 3 rows which are headers/buttons)
                for row in rows[3:]:
                    cols = row.find_all(['th', 'td'])
                    if cols:
                        # Clean html spaces (\xa0) and multiple spaces
                        clean_cols = [re.sub(r'\s+', ' ', c.text.replace('\xa0', ' ').strip()) for c in cols]
                        data.append(clean_cols)
                        
                return {
                    'symbol': dw_symbol,
                    'dates': dates,
                    'data': data
                }
            else:
                print(f"Table not found for {dw_symbol}")
                return None
    except Exception as e:
        print(f'Error fetching {dw_symbol}: {e}')
        return None

if __name__ == '__main__':
    # Test with AAV13C2610A
    res = scrape_kgi_dw_table('AAV13C2610A')
    if res:
        print(f"Symbol: {res['symbol']}")
        print(f"Dates: {res['dates']}")
        for row in res['data'][:5]:
            print(row)
