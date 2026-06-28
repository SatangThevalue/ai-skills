---
name: innovestx-open-api
description: Guide and implementation details for using InnovestX Digital Asset Open API.
prerequisites:
  - Valid InnovestX account with digital asset portfolio
  - API Key and Secret generated via trade.innovestxonline.com
  - NodeJS/Python for implementation
---

# InnovestX Digital Asset Open API Integration

This skill provides guidelines and implementation details for integrating with the InnovestX Digital Asset Open API. It allows programmatic access to trading, market data, account balances, and wallet management.

## 1. Authentication Details

The API uses HMAC SHA256 signatures for authentication.

**Base URL:** `https://api.innovestxonline.com/api/v1/digital-asset/`

### Required Headers
- `X-INVX-APIKEY`: (String 64) Your API Key
- `X-INVX-SIGNATURE`: (String) HMAC SHA256 signature
- `X-INVX-REQUEST-UID`: (String 36) UUID for the request
- `X-INVX-TIMESTAMP`: (String 13) UTC timestamp in milliseconds (Must be within 150 seconds of server time)
- `Content-Type`: `application/json`

### Signature Generation Rule
The `X-INVX-SIGNATURE` is created using `HMAC-SHA256` with your **API Secret**.
The string to sign MUST be concatenated exactly in this order:
`API Key` + `HTTP Method` (uppercase) + `Host` (lowercase) + `Path` (with leading slash) + `Query String` (exact) + `Content-Type` + `Request UID` + `Timestamp` + `Request Body` (raw JSON string).

## 2. Implementations

### Python Implementation Example

```python
import hmac
import hashlib
import json
import uuid
import time
import requests

API_KEY='***'
API_SECRET='***'
HOST = 'api.innovestxonline.com'

def make_request(method, path, body=None, query=''):
    request_uid = str(uuid.uuid4())
    timestamp = str(int(time.time() * 1000))
    content_type = 'application/json'
    
    body_str = json.dumps(body) if body else ''
    if body_str == '{}': body_str = ''
    
    # Construct string to sign
    content_to_sign = (
        API_KEY + 
        method.upper() + 
        HOST.lower() + 
        path + 
        query + 
        content_type + 
        request_uid + 
        timestamp + 
        body_str
    )
    
    # Generate signature
    signature = hmac.new(
        API_SECRET.encode('utf-8'),
        content_to_sign.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    headers = {
        'Content-Type': content_type,
        'X-INVX-APIKEY': API_KEY,
        'X-INVX-SIGNATURE': signature,
        'X-INVX-REQUEST-UID': request_uid,
        'X-INVX-TIMESTAMP': timestamp
    }
    
    url = f"https://{HOST}{path}{'?' + query if query else ''}"
    
    if method.upper() == 'POST':
        response = requests.post(url, headers=headers, data=body_str)
    elif method.upper() == 'GET':
        response = requests.get(url, headers=headers)
        
    return response.json()

# Example: Get Orderbook
response = make_request('POST', '/api/v1/digital-asset/orderbook/lvl2', {'symbol': 'ETHTHB'})
print(response)
```

### NodeJS Implementation Example

```javascript
const axios = require("axios");
const uuid = require("uuid");
const CryptoJS = require("crypto-js");

const apiKey = "YOUR_API_KEY";
const apiSecret = "YOUR_API_SECRET";
const host = "api.innovestxonline.com";

async function makeRequest(method, path, data = {}, query = "") {
    const requestUId = uuid.v4();
    const timestamp = new Date().getTime().toString();
    const contentType = "application/json";
    
    const bodyStr = Object.keys(data).length > 0 ? JSON.stringify(data) : "";

    const contentToSign = apiKey + method.toUpperCase() + host.toLowerCase() + path + query + contentType + requestUId + timestamp + bodyStr;
    const signature = CryptoJS.enc.Hex.stringify(CryptoJS.HmacSHA256(contentToSign, apiSecret));

    const headers = {
        "Content-Type": contentType,
        "X-INVX-APIKEY": apiKey,
        "X-INVX-SIGNATURE": signature,
        "X-INVX-REQUEST-UID": requestUId,
        "X-INVX-TIMESTAMP": timestamp
    };

    const url = `https://${host}${path}${query ? "?" + query : ""}`;

    try {
        const response = await axios({
            method: method,
            url: url,
            headers: headers,
            data: bodyStr
        });
        return response.data;
    } catch (error) {
        console.error("API Error:", error.response ? error.response.data : error.message);
        throw error;
    }
}

// Example: Get Orderbook
makeRequest('POST', '/api/v1/digital-asset/orderbook/lvl2', { symbol: "ETHTHB" })
    .then(console.log);
```

## 3. Important Notes & Pitfalls

- **Timestamp Synchronization:** The `X-INVX-TIMESTAMP` must be within 150 seconds of the server's UTC time. If you receive an error `4010` - `4012`, check your system clock synchronization.
- **API Secret:** It is shown ONLY ONCE during creation on the website. Store it securely.
- **IP Whitelisting:** It is recommended to restrict the API key to trusted IP addresses when generating the key on the website.
- **Required Permissions:** Ensure your API key has the correct permissions (Trading, Deposits, Withdraws, Read) for the endpoints you intend to use.
- **Send Order Parameter Rules:** When calling `/order/send`, you must provide either `quantity` OR `value`, not both. Wait time in force (`timeInForce`) should be `1` (Good Till Cancelled). Order types: `1`=Market, `2`=Limit. Sides: `0`=Buy, `1`=Sell.

## 4. API Endpoints Reference

### Market Data
- **Subscribe Level 2:** `POST /api/v1/digital-asset/orderbook/lvl2`
- **Subscribe Ticker:** `POST /api/v1/digital-asset/ticker/subscribe`

### Order Management
- **Send Order:** `POST /api/v1/digital-asset/order/send`
- **Cancel Order:** `POST /api/v1/digital-asset/order/cancel`
- **Get Open Orders:** `GET /api/v1/digital-asset/order/open/inquiry`
- **Get Order History:** `POST /api/v1/digital-asset/order/history`
- **Get Estimate Fee:** `POST /api/v1/digital-asset/order/estimate-fee`

### Standard Error Codes
- **4000/4001:** Reject transaction
- **4002:** Invalid API Key
- **4005:** Invalid Signature
- **4010/4011:** Timestamp issues (format or >150s diff)
- **4014/4015:** Missing limitPrice, quantity, or value
- **4019:** Insufficient Balance
- **4042/4043:** Symbol/Product not found
