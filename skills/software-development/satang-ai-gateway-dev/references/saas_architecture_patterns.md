# Satang AI SaaS Architecture Patterns

## 1. Domain & URL Separation (Subdomain Pattern)
For production, separate the frontend and backend using Traefik subdomains to simplify CORS, security, and webhook ingestion:
- **Marketing/SEO:** `https://satang.ai` (Redirects to `www` or `app`)
- **Frontend App:** `https://app.satang.ai` (Next.js 16+ with Better-Auth)
- **Backend API:** `https://api.satang.ai` (FastAPI Gateway)

## 2. Environment Variable Standards
### Frontend (Next.js)
```env
BETTER_AUTH_URL=https://app.satang.ai
NEXT_PUBLIC_API_URL=https://api.satang.ai
```
### Backend (FastAPI)
```env
FRONTEND_CORS_ORIGINS="https://app.satang.ai,https://satang.ai,http://localhost:3000"
```
*FastAPI must configure `CORSMiddleware` using `allow_origins=FRONTEND_CORS_ORIGINS` and `allow_credentials=True` to accept Better-Auth session cookies.*

## 3. Multi-Tenant URL Routing (Next.js App Router)
Use `orgSlug` as the root path parameter for authenticated workspace routes to ensure context is always present.
- `/` (Public Landing)
- `/auth/login` (Public Auth)
- `/:orgSlug/dashboard` (Workspace Overview)
- `/:orgSlug/billing` (Subscription & Beam Checkout integration)
- `/:orgSlug/[module]/...` (Module-specific routes, e.g., `/ai-content/create`, `/merchant/transactions`)

## 4. Modular SaaS Database & Quota Design
Instead of checking tiers dynamically during AI execution, manage access via a Quota system:
- **Packages:** Define Modules (`personal_finance`, `ai_content`) and Tiers (`free`, `pro`, `unlimited`).
- **Organization Subscriptions:** Link an Organization to a Package.
- **Usage Quotas:** Allocate quotas based on the subscribed tier upon creation/renewal.
- **Execution Flow:** 
  1. FastAPI endpoint is called.
  2. Check `usage_quota` for the specific feature (e.g., `ai_post`).
  3. If quota > 0, dispatch to Prefect and mark task as `pending`.
  4. On Prefect completion, decrement the quota and update task to `completed`.
