---
name: line-mini-app-liff-serverless
description: Create LINE MINI Apps using LIFF based on the SupremeTech serverless approach. Use when planning, designing, or building a LINE MINI App with LIFF, especially for membership management or m-commerce without a dedicated backend server.
---

# Create LINE MINI App with LIFF (Serverless Approach)

## Overview
This skill provides a framework and best practices for developing LINE MINI Apps using the LINE Front-end Framework (LIFF), specifically adopting a serverless architecture. This approach is highly effective for membership management, digital point cards, and mobile commerce (m-commerce), enabling high scalability for promotions and requests.

## Core Concepts & Technologies
*   **LIFF (LINE Front-end Framework):** A web application platform provided by LINE. It allows apps to run within the LINE messenger, access user data (like LINE user ID), and send messages on behalf of the user.
*   **LINE MINI App:** A lightweight application running inside LINE, preventing the need for users to download separate native apps.
*   **Serverless Architecture:** Utilizing cloud services (like AWS Lambda, API Gateway) instead of traditional server infrastructure to handle backend logic. This ensures scalability during high-traffic promotions.
*   **Typical Tech Stack:** TypeScript, AWS (Serverless framework), Next.js / React (for frontend).

## Key Features of a Membership LINE MINI App
When designing a membership or point-card system on LINE, consider these core features:

1.  **Interactive Rich Menu:**
    *   Acts as the central hub (dashboard).
    *   Provides quick links to services, external websites, reservation pages, and the digital points card.
2.  **Digital Points Card / Membership Card:**
    *   Accessible directly from the Rich Menu.
    *   Displays barcodes/QR codes for in-store scanning.
    *   Shows current point balance and membership tier.
3.  **M-Commerce & Rewards:**
    *   In-app purchasing capabilities.
    *   Point accumulation tracking.
    *   Redemption mechanisms for gifts, discounts, or perks.
4.  **Exclusive Engagement & Brand Updates:**
    *   Gated special offers (requires users to 'Follow' the Official Account).
    *   Automated push messages for new campaigns and products via LINE Messaging API.

## Implementation Workflow (Serverless approach)

### 1. Setup & Registration
*   Register a LINE Channel (LINE Login channel) in the LINE Developers Console.
*   Add a LIFF app to the channel to get the `liffId`.
*   Apply for LINE MINI App status (requires review by LINE if publishing publicly).

### 2. Frontend Development (LIFF App)
*   Initialize the LIFF SDK in your web application (e.g., Next.js).
    ```javascript
    import liff from '@line/liff';

    async function initializeLiff() {
        try {
            await liff.init({ liffId: process.env.NEXT_PUBLIC_LIFF_ID });
            if (!liff.isLoggedIn()) {
                liff.login();
            } else {
                // User is logged in, get profile data
                const profile = await liff.getProfile();
                console.log(profile.userId);
            }
        } catch (error) {
            console.error('LIFF initialization failed', error);
        }
    }
    ```
*   Build the UI for the digital membership card, product listings, and reward redemption. Ensure it is heavily optimized for mobile viewports.

### 3. Backend (Serverless via AWS)
*   Instead of a traditional Node.js/Express server, set up AWS API Gateway routing to AWS Lambda functions (written in TypeScript).
*   **Endpoints needed:**
    *   Verify LINE user identity (using access tokens passed from the LIFF frontend).
    *   Fetch user point balance / membership tier from the database (e.g., DynamoDB).
    *   Process transactions (adding/deducting points).
*   *Security Note:* Never trust the `userId` sent directly from the client. Always verify the access token on the backend using the LINE Social API.

### 4. Rich Menu Configuration
*   Design a visual Rich Menu image.
*   Use the LINE Messaging API to create the Rich Menu, upload the image, set the tap actions (linking to the LIFF URL), and set it as the default menu for users.

## Pitfalls & Best Practices
*   **Token Verification:** Crucial for serverless. The LIFF app must pass the `accessToken` or `idToken` to your serverless functions. The function must validate this token with LINE's servers before returning any sensitive user data (like point balances).
*   **Cold Starts:** In a serverless architecture (like AWS Lambda), cold starts can cause latency. Optimize your Lambda functions (e.g., keep package sizes small, consider provisioned concurrency for high-traffic periods).
*   **LIFF Browser Limitations:** LIFF runs in an in-app browser. Avoid relying on features that require multiple tabs or complex external popups. Keep the flow contained within the LIFF window.
*   **State Management:** Since users might close the LINE app at any time, ensure critical state (like a shopping cart or points deduction) is immediately synced to the backend rather than relying solely on local storage.

## References
*   SupremeTech Case Study: LINE MINI App for Membership Management with LIFF
*   [Official LIFF Documentation](https://developers.line.biz/en/docs/liff/)
*   [LINE MINI App Documentation](https://developers.line.biz/en/docs/line-mini-app/)