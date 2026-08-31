import sys
import json
from settrade_v2 import Investor

def main():
    if len(sys.argv) != 5:
        print(json.dumps({"error": "Usage: python check_sandbox.py <APP_ID> <APP_SECRET> <EQUITY_ACC> <DERIV_ACC>"}))
        sys.exit(1)

    app_id = sys.argv[1]
    app_secret = sys.argv[2]
    eq_acc = sys.argv[3]
    der_acc = sys.argv[4]

    res = {}

    try:
        investor = Investor(
            app_id=app_id,
            app_secret=app_secret,
            broker_id="SANDBOX",
            app_code="SANDBOX",
            is_auto_queue=False
        )
        res["Auth"] = "Success"
    except Exception as e:
        res["Auth"] = f"Failed: {str(e)}"
        print(json.dumps(res, indent=2))
        sys.exit(1)

    try:
        equity = investor.Equity(account_no=eq_acc)
        eq_info = equity.get_account_info()
        res["Equity"] = {
            "Line Available": eq_info.get("lineAvailable"),
            "Cash Balance": eq_info.get("cashBalance")
        }
    except Exception as e:
        res["Equity"] = f"Error: {str(e)}"

    try:
        deriv = investor.Derivatives(account_no=der_acc)
        der_info = deriv.get_account_info()
        res["Derivatives"] = {
            "Equity Balance": der_info.get("equity")
        }
    except Exception as e:
        res["Derivatives"] = f"Error: {str(e)}"

    try:
        market = investor.MarketData()
        quote = market.get_quote_symbol("PTT")
        res["MarketData_PTT"] = quote.get("last")
    except Exception as e:
        res["MarketData_PTT"] = f"Error (Likely outside market hours): {str(e)}"

    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
