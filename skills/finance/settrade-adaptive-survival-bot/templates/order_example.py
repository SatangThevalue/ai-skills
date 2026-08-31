from settrade_v2 import Investor

APP_ID = "YOUR_APP_ID"
APP_SECRET = "YOUR_APP_SECRET"
APP_CODE = "SANDBOX" 
BROKER_ID = "SANDBOX"
PIN = "000000"

investor = Investor(
    app_id=APP_ID,
    app_secret=APP_SECRET,
    app_code=APP_CODE,
    broker_id=BROKER_ID,
    is_auto_queue=False
)
equity = investor.Equity(account_no="satang-E")

# RIGHT WAY to place a Market Order (กวาดราคาตลาด)
# MP-MKT MUST be paired with FOK or IOC.
res_market = equity.place_order(
    pin=PIN, 
    side="Buy", 
    symbol="PTT", 
    volume=100, 
    price=0, 
    price_type="MP-MKT",
    validity_type="FOK" 
)

# RIGHT WAY to place a Limit Order (รอราคาที่ตั้งไว้)
# validity_type="Day" is allowed here because the price is specified.
res_limit = equity.place_order(
    pin=PIN, 
    side="Buy", 
    symbol="PTT", 
    volume=100, 
    price=35.00, 
    price_type="Limit",
    validity_type="Day"
)