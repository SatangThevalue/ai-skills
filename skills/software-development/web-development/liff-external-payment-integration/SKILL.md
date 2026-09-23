---
name: liff-external-payment-integration
description: Integrate external payments in LINE LIFF apps.
version: 0.1.0
metadata:
  hermes:
    tags: [LINE, LIFF, Payments, UX]
---

# LIFF External Payment Integration

This skill outlines how to integrate external payment gateways (such as BeamCheckout QR PromptPay) into LINE LIFF and LINE Mini Apps. It specifically addresses how to bypass LINE's internal browser sandbox to enable deep-linking to banking apps, and sets up a secure webhook-driven plan upgrade flow. It does not cover generic payment gateway merchant registration.

## When to Use
- When users need to scan or pay with TH-QR PromptPay or global cards inside a LINE LIFF app.
- When you want to resolve the "PromptPay scanning friction" (requiring screenshots to scan within the same device).
- When automating plan upgrades (e.g., Free to Pro) based on payment gateway webhooks.

## Prerequisites
- A configured LINE LIFF ID.
- Payment gateway credentials (e.g., `BEAM_MERCHANT_ID` and `BEAM_API_KEY`).
- Database schema containing `user_subscription` or similar membership/billing tables.

## How to Run
- Use the `write_file` tool to create server-side payment generation and webhook routes.
- Use the `patch` tool to inject external redirect buttons on dashboard components.
- Use the `terminal` tool to build, deploy, and verify server logs.

## Quick Reference
- Force open in native mobile browser: `liff.openWindow({ url: paymentUrl, external: true })`
- BeamCheckout Payment Link Endpoint: `POST /api/v1/payment-links`
- Payload reference schema for PromptPay billing:
  ```json
  {
    "order": { "currency": "THB", "netAmount": 149.00, "referenceId": "ORDER_ID" },
    "linkSettings": { "qrPromptPay": { "isEnabled": true } }
  }
  ```

## Procedure

1. **Create Backend Checkout API**
   Implement an API route (e.g. `/api/subscription/checkout`) that generates a payment link from the gateway. Store user identifiers inside the payment's metadata/reference ID:
   ```typescript
   // apps/frontend/src/app/api/subscription/checkout/route.ts
   const authHeader = `Basic ${Buffer.from(`${MERCHANT_ID}:${API_KEY}`).toString("base64")}`;
   const response = await fetch("https://playground.api.beamcheckout.com/api/v1/payment-links", {
     method: "POST",
     headers: { "Authorization": authHeader, "Content-Type": "application/json" },
     body: JSON.stringify({
       order: { currency: "THB", netAmount: 149.00, referenceId: `SUB_PRO_${userId}_${Date.now()}` },
       linkSettings: { qrPromptPay: { isEnabled: true }, card: { isEnabled: false } },
       redirectUrl: "https://your-domain.app/dashboard?payment=success"
     })
   });
   const data = await response.json();
   ```

2. **Trigger Link from Front-End via External Window**
   In the user interface component, fetch the URL and check if the user is inside LINE client before redirecting:
   ```typescript
   const handlePayment = async () => {
     const res = await fetch("/api/subscription/checkout", { method: "POST" });
     const data = await res.json();
     if (data.success && data.url) {
       if (liff && liff.isInClient()) {
         liff.openWindow({
           url: data.url,
           external: true // ⚡ CRITICAL: Forces opening in default Safari/Chrome to enable Bank App-switching
         });
       } else {
         window.location.href = data.url;
       }
     }
   };
   ```

3. **Install Webhook Route for Database Upgrades**
   Write a callback route (e.g. `/api/subscription/webhook`) that listens to payments:
   ```typescript
   export async function POST(req: NextRequest) {
     const data = await req.json();
     if (data.status === "PAID") {
       const referenceId = data.order?.referenceId || "";
       if (referenceId.startsWith("SUB_PRO_")) {
         const parts = referenceId.split("_");
         const userId = parts.slice(2, parts.length - 1).join("_");
         // Perform database update query to upgrade plan_tier to 'pro'
       }
     }
     return NextResponse.json({ success: true });
   }
   ```

## Pitfalls
- **LINE Browser Trapping:** Redirecting using standard `window.location.href` keeps the payment window inside LINE's browser. This blocks native mobile deep-linking buttons ("Open Banking App"), forcing users to screenshot and scan. Always use `liff.openWindow({ external: true })`.
- **Better-Auth Client Limitations:** Client-side updates to credential schemas (like changing passwords or linking credentials) will fail due to client security context limitations. Always delegate credential mutations (such as linking passwords to an OAuth/LINE-only account) to a secure server-side endpoint.
- **String Parsing on User ID:** When parsing reference IDs (e.g., split by `_`), remember that User IDs can contain hyphens or other symbols. Always slice properly (`parts.slice(start, end).join("_")`) to prevent truncated IDs.
- **Thai Language Excel Support in CSV:** When exporting financial/payment reports in Thai language to CSV format, always prepend the Byte Order Mark (BOM) character `\uFEFF` before writing the CSV string. Excel will otherwise render Thai characters as corrupted/foreign letters (ต่างด้าว).
- **PDPA Erasure Safeguard:** When implementing account deletion (PDPA Right to Erasure), protect against accidental triggers by requiring the user to type a specific confirmation phrase (e.g. `DELETE-SATANG`) and double-confirm via alert box before initiating hard deletes across all relational tables.
- **Expandable Accordion Cards:** Keep settings screens compact on mobile viewports by bundling advanced administrative options (like Account Linking and PDPA Erasure) into expandable/collapsible accordion panels.
- **Tax Bracket Computation (Thailand):** Personal income tax simulations must dynamically classify income into standard sections (e.g. 40(1) to 40(8)) and calculate progressive tax brackets according to Thai tax laws (0% for <=150k, 5% up to 300k, 10% up to 500k, 15% up to 750k, 20% up to 1m, 25% up to 2m, 30% up to 5m, and 35% above).
- **Mobile Scrolling & UX:** When converting database layouts or tables for touch-screens, do not use hover-dependent elements (like opacity changes for edit/delete buttons). Make actions persistently visible on mobile screens, and transition cramped tabular views into vertical card lists to prevent text clipping.

## Verification
Simulate a webhook payload using the `terminal` tool:
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"status":"PAID","order":{"referenceId":"SUB_PRO_test-user-id_12345"}}' \
  http://localhost:3000/api/subscription/webhook
```
Verify that the database changes reflect the updated membership state.
