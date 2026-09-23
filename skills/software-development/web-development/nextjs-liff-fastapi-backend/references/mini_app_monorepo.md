# Feature-Sliced Design (Mini-App Monorepo Pattern)

When building complex Next.js + FastAPI SaaS applications with multiple distinct features, standard directory structures can become tangled. 

A "Mini-App" or Feature-Sliced approach isolates business logic into dedicated folders, making development cleaner and permissions easier to enforce.

## Next.js Frontend Structure
Instead of putting all pages flat in `app/`, group by feature under `src/features`:

```text
apps/frontend/
├── src/
│   ├── app/            # Only routing components (page.tsx, layout.tsx)
│   ├── features/       # 🚀 The Mini-Apps
│   │   ├── core/       # Authentication, Dashboard, Billing
│   │   ├── ai-content/ # Module 1: AI Tools
│   │   ├── merchant/   # Module 2: Merchant Accounting
│   ├── shared/         # Reusable UI (buttons, cards), Hooks
```

## FastAPI Backend Structure
Mirror the frontend domains in your API routing:

```text
apps/backend/
├── src/
│   ├── api/
│   │   ├── core/       # /api/users, /api/auth
│   │   ├── ai_content/ # /api/content/generate
│   │   ├── merchant/   # /api/merchant/transactions
│   ├── models/         # SQLModel schemas
```

## Traefik Gateway Routing
Use PathPrefix to securely route API calls from the frontend domain to the backend without complex CORS setups:

```yaml
http:
  routers:
    saas-api:
      rule: "Host(`app.example.com`) && (PathPrefix(`/api`) || PathPrefix(`/webhooks`))"
      service: backend-api
    saas-web:
      rule: "Host(`app.example.com`)"
      service: frontend-web
```
This ensures `/api/*` goes to FastAPI (port 8000), while everything else goes to Next.js (port 3000).
