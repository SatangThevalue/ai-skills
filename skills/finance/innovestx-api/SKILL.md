---
name: innovestx-api
description: InnovestX Digital Asset Open API integration guide and Python client implementation.
tags:
  - finance
  - crypto
  - api
  - innovestx
  - trading
---

# InnovestX Open API Skill

This skill provides instructions, endpoints, and code for integrating with the InnovestX Digital Asset RESTful API.

## Base URL
`https://api.innovestxonline.com/api/v1/digital-asset`

## Authentication

InnovestX API requires specific headers and an HMAC-SHA256 signature for every request.

### Mandatory Headers:
- `X-INVX-APIKEY`: Your 64-character API key
- `X-INVX-SIGNATURE`: HMAC SHA256 signature
- `X-INVX-REQUEST-UID`: Unique UUID string for the request
- `X-INVX-TIMESTAMP`: UTC timestamp in milliseconds (must be within 150s of server time)
- `Content-Type`: `application/json`

### Signature Generation
The string to sign must be formatted exactly as:
`X-INVX-APIKEY` + `HTTP Verb` + `url.host` + `url.path` + `url.query` + `Content-Type` + `X-INVX-REQUEST-UID` + `X-INVX-TIMESTAMP` + `request.body`

## Python Client Implementation

Save this script as `innovestx_client.py`:

```python
import time
import uuid
import hmac
import hashlib
import json
import requests

class InnovestXClient:
    def __init__(self, api_key: str, api_secret: str, env="prod"):
        self.api_key = api_key
        self.api_secret = api_secret
        if env == "dev":
            self.host = "api-dev.innovestxonline.com"
        else:
            self.host = "api.innovestxonline.com"
            
        self.base_path = "/api/v1/digital-asset"

    def _generate_signature(self, method: str, path: str, query: str, content_type: str, request_uid: str, timestamp: str, body_str: str) -> str:
        content_to_sign = f"{self.api_key}{method}{self.host}{path}{query}{content_type}{request_uid}{timestamp}{body_str}"
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            content_to_sign.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature

    def request(self, method: str, endpoint: str, body: dict = None, query: str = ""):
        path = f"{self.base_path}{endpoint}"
        url = f"https://{self.host}{path}"
        
        request_uid = str(uuid.uuid4())
        timestamp = str(int(time.time() * 1000))
        content_type = "application/json"
        
        # InnovestX expects no body or empty string for GET requests
        body_str = json.dumps(body) if body is not None and method in ['POST', 'PUT'] else ""
        
        signature = self._generate_signature(method, path, query, content_type, request_uid, timestamp, body_str)
        
        headers = {
            "Content-Type": content_type,
            "X-INVX-REQUEST-UID": request_uid,
            "X-INVX-TIMESTAMP": timestamp,
            "X-INVX-SIGNATURE": signature,
            "X-INVX-APIKEY": self.api_key,
            "Accept-language": "EN"
        }
        
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, data=body_str)
            
        return response.json()

# Example Usage
# client = InnovestXClient("YOUR_API_KEY", "YOUR_API_SECRET")
# print(client.request("GET", "/account/balance/inquiry"))
# print(client.request("POST", "/orderbook/lvl2", body={"symbol": "BTCTHB"}))
```

## Available Endpoints
*Prefix all endpoints with `/api/v1/digital-asset`*

### Market Data
- `POST /orderbook/lvl2` - Subscribe to Level 2 orderbook (Body: `{"symbol": "BTCTHB", "depth": 100}`)
- `POST /ticker/subscribe` - Get 1-minute ticker data (Body: `{"symbol": "BTCTHB"}`)

### Account Management
- `GET /account/balance/inquiry` - Get account balances and holds.
- `POST /account/trade/inquiry` - Get trade history.

### Order Management
- `POST /order/send` - Send a buy/sell order. 
  - Required body: `symbol`, `timeInForce` (1=GTC), `side` (0=Buy, 1=Sell), `orderType` (1=Market, 2=Limit). For Limit, `limitPrice` is required. Provide either `quantity` or `value`.
- `POST /order/cancel` - Cancel an open order (Body: `{"orderId": "..."}`).
- `GET /order/open/inquiry` - List open orders.
- `POST /order/history/inquiry` - Get order history (Body: `{"symbol": "BTCTHB"}`).
- `POST /order/fee/inquiry` - Estimate transaction fee (Body: `symbol`, `amount`, `price`, `side`).

### Market Info / Products
- `GET /products` - Get array of products available (e.g. BTC, THB).
- `GET /symbols` - Get array of trading symbols (e.g. BTCTHB) and their increments.
- `POST /product/fee/tier` - Get product fee tier.
- `POST /symbol/fee/tier` - Get symbol fee tier.

### Deposits & Withdrawals
- `POST /deposit/fiat/create` - Deposit fiat.
- `POST /deposit/address/inquiry` - Get deposit wallet address.
- `GET /deposit/inquiry` - Get deposit ticket status.
- `GET /deposit/all/inquiry` - Get all deposit tickets.
- `POST /withdraw/crypto/create` - Withdraw crypto to external wallet.
- `POST /withdraw/fiat/create` - Withdraw fiat to bank.
- `POST /withdraw/address/inquiry` - Get withdraw wallet addresses/networks.
- `GET /withdraw/inquiry` - Get withdraw status.
- `GET /withdraw/all/inquiry` - Get all withdraws.
- `POST /withdraw/cancel` - Cancel a withdrawal.
- `POST /withdraw/fee` - Get withdrawal fee.

## Pitfalls & Best Practices
1. **Timestamp:** The `X-INVX-TIMESTAMP` must be within 150 seconds of the server's UTC time. Ensure the system clock is synchronized via NTP.
2. **Signature Ordering:** The string to sign uses absolute exact matching. Do not add extra spaces. Ensure `method` is uppercase (`GET`, `POST`) and `url.host` is lowercase.
3. **Empty Body on GET:** For GET requests, the `request.body` part of the signature string should be completely empty (not `"{}"`).
4. **Order Types:** `timeInForce`: 1=GTC, 3=IOC, 4=FOK. `side`: 0=Buy, 1=Sell. `orderType`: 1=Market, 2=Limit.
5. **Quantity vs Value:** When sending an order, you must provide either `quantity` (amount of crypto) or `value` (total fiat cost), but not both if using market orders. Limit orders usually require `quantity` and `limitPrice`.
