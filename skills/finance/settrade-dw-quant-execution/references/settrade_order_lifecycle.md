# Settrade Open API: Order Execution Lifecycle & Sandbox Recipes

Verified implementation recipes for order placement, reconciliation, cancellation, and error handling on the SET / Settrade Open API v2.

---

## 1. Authentication & Account Scope

In Thailand SET, **Derivative Warrants (DW) are classified as equities**, not derivatives:
- **DW / Equity Account:** `satang-E` (`investor.Equity(account_no="satang-E")`)
- **Futures / Options Account:** `satang-D` (`investor.Derivatives(account_no="satang-D")`)
- **Default PIN:** `000000`

```python
import os
from settrade_v2 import Investor

investor = Investor(
    app_id=os.getenv("SETTRADE_APP_ID"),
    app_secret=os.getenv("SETTRADE_APP_SECRET"),
    broker_id="SANDBOX",
    app_code="SANDBOX",
    is_auto_queue=False
)
equity = investor.Equity(account_no=os.getenv("SETTRADE_ACCOUNT_NO", "YOUR_ACCOUNT_NO"))
```

---

## 2. Order Placement (Limit Order Recipe)

```python
order = equity.place_order(
    pin="000000",
    side="Buy",           # Must be Title Case: "Buy" or "Sell"
    symbol="PTT",         # Stock or DW symbol (e.g. "PTT01C2608A")
    volume=100,           # Must be multiple of 100 (Board Lot)
    price=52.00,          # Must fall within day's floor/ceiling and 10 spreads of last price
    price_type="Limit",   # "Limit", "ATO", "ATC", "MP-MKT", "MP-MTL"
    validity_type="Day"   # "Day", "FOK", "IOC"
)
print("Order Number:", order.get("orderNo"))
```

### Response Payload Shape
```json
{
  "orderNo": "66F68O62GH",
  "accountNo": "satang-E",
  "symbol": "PTT",
  "side": "Buy",
  "price": 52.0,
  "vol": 100,
  "status": "OF",
  "showOrderStatusMeaning": "Offline order",
  "terminalType": "API_SANDBOX",
  "canCancel": true,
  "canChangePriceVol": true
}
```

---

## 3. Order Reconciliation & Inquiry

```python
orders = equity.get_orders()
for o in orders:
    order_no = o.get("orderNo")
    symbol = o.get("symbol")
    side = o.get("side")
    price = o.get("price")
    vol = o.get("vol")
    matched = o.get("matched", 0)
    status_meaning = o.get("showOrderStatusMeaning")
    print(f"[{order_no}] {side} {vol} {symbol} @ {price} | Status: {status_meaning} | Matched: {matched}")
```

---

## 4. Order Cancellation

```python
cancel_result = equity.cancel_order(order_no="66F68O62GH", pin="000000")
print("Cancelled:", cancel_result)
```

---

## 5. OSS Rejection Diagnosis & Fixes

1. **`[OSS] Order price exceeds 10 spread(s) from last price`:**
   - **Cause:** Settrade Order Sending Server enforces a collar of maximum 10 price spreads from the current last traded price.
   - **Fix:** Limit order price must stay within $\pm 10$ ticks of the active quote.

2. **`Price should between X to Y`:**
   - **Cause:** Order price violated the exchange daily floor and ceiling bounds (typically $\pm 30\%$ from previous close).
   - **Fix:** Verify prices against `floor` and `ceiling` attributes before dispatching.

3. **`Cannot place Market order when validity is not FOK/IOC`:**
   - **Cause:** The SET exchange forbids `MP-MKT` paired with `validity_type="Day"`.
   - **Fix:** Always pair `MP-MKT` with `FOK` (Fill-or-Kill) or `IOC` (Immediate-or-Cancel). For standard day orders, use `price_type="Limit"`.
