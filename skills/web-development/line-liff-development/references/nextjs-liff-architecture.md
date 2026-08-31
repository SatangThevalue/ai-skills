# Next.js 16 + LIFF App Architecture Reference

Built and verified in session 2026-06-30. Stack: Next.js 16.2.9, React 19, TypeScript strict, Tailwind v4, @line/liff, Zod v4, react-hook-form, recharts, sonner, lucide-react, date-fns.

## Environment Variables Pattern

```
# Public (browser-visible)
NEXT_PUBLIC_APP_NAME=
NEXT_PUBLIC_APP_URL=          # must match LIFF Endpoint URL exactly
NEXT_PUBLIC_LIFF_ID=          # format: 1234567890-AbCdEfGh
NEXT_PUBLIC_DEFAULT_LOCALE=th-TH

# Server-only (never exposed)
N8N_LIFF_API_URL=             # webhook for LIFF ops
N8N_MEMBERSHIP_API_URL=       # webhook for membership
N8N_ADMIN_API_URL=            # webhook for admin
N8N_API_SHARED_SECRET=        # validated by n8n on every call
ADMIN_ACCESS_TOKEN=           # simple MVP admin gate
NODE_ENV=
```

## File Structure (minimal production-ready)

```
src/
├── app/
│   ├── layout.tsx                   # Root layout, fonts, Providers
│   ├── globals.css                  # Tailwind v4 @import + CSS vars
│   ├── page.tsx                     # Home (balance hero, recent tx)
│   ├── categories/page.tsx          # CRUD with icon/color picker modal
│   ├── budgets/page.tsx             # Progress bars, month selector
│   ├── summary/page.tsx             # recharts BarChart, top categories
│   ├── membership/page.tsx          # Plan cards, checkout redirect
│   ├── confirm-transaction/page.tsx # AI tx confirm/reject (Suspense wrapped)
│   ├── admin/page.tsx               # Token-gated dashboard
│   └── api/
│       ├── categories/route.ts      # GET, POST
│       ├── categories/[id]/route.ts # PUT, DELETE
│       ├── budgets/route.ts
│       ├── budgets/[id]/route.ts
│       ├── transactions/route.ts
│       ├── transactions/pending/route.ts
│       ├── transactions/confirm/route.ts
│       ├── transactions/reject/route.ts
│       ├── summary/route.ts
│       ├── membership/profile/route.ts
│       ├── membership/plans/route.ts
│       ├── membership/status/route.ts
│       ├── membership/checkout/route.ts
│       ├── admin/stats/route.ts
│       └── admin/users/route.ts
├── components/
│   ├── Providers.tsx               # LiffProvider + Sonner Toaster
│   ├── layout/
│   │   ├── BottomNav.tsx           # 5-tab mobile nav
│   │   └── PageHeader.tsx          # Sticky header with avatar
│   └── ui/
│       ├── Button.tsx              # CVA variants (default/outline/ghost/income/expense)
│       ├── Card.tsx                # Card + CardHeader + CardTitle + CardContent
│       ├── Input.tsx               # Input + Textarea + Select (all forwardRef)
│       ├── Badge.tsx               # variant per type/plan
│       ├── Loading.tsx             # Loading (spinner) + PageLoading (full-page logo)
│       └── ProgressBar.tsx         # auto-variant safe/warning/danger
├── contexts/
│   └── LiffContext.tsx             # isReady, isLoggedIn, profile, idToken, login, logout
└── lib/
    ├── types.ts                    # All domain types (no Zod deps)
    ├── schemas.ts                  # Zod v4 schemas + inferred types
    ├── utils.ts                    # cn(), formatCurrency, formatDate, getBudgetStatus
    ├── liff.ts                     # SDK wrapper — "use client", singleton init guard
    ├── api-client.ts               # Frontend → /api/* fetch wrappers
    └── n8n-proxy.ts                # Server-only → n8n webhook proxy
```

## n8n Action Convention

Every call to n8n uses a single webhook URL per domain + `action` field to route:

```json
// Request to N8N_LIFF_API_URL
{
  "action": "list_categories",     // or create_category, update_category, delete_category
  "idToken": "<LINE ID Token>",    // n8n verifies and resolves userId
  "year": 2026,                    // extra payload fields
  "month": 6
}
// Header: X-API-Secret: <N8N_API_SHARED_SECRET>
```

Actions used:
- `list_categories`, `create_category`, `update_category`, `delete_category`
- `list_budgets`, `create_budget`, `update_budget`, `delete_budget`
- `list_transactions`, `create_transaction`, `list_pending_transactions`, `confirm_transaction`, `reject_transaction`
- `get_summary`
- `get_profile`, `list_plans`, `get_membership_status`, `create_checkout`
- `get_admin_stats`, `get_admin_users`

## Key Build Fixes Found

| Error | Cause | Fix |
|---|---|---|
| `useSearchParams()` prerender error | Next.js 16 requires Suspense | Split into inner + wrapper with `<Suspense>` |
| `Formatter<ValueType>` recharts TS error | `value` is `ValueType \| undefined` | `typeof value === "number" ? fn(value) : String(value)` |
| Zod `errorMap` TS2769 | Zod v4 removed `errorMap` option | Remove options object from `z.enum()` |
| Zod `invalid_type_error` TS2353 | Zod v4 API change | Use `.positive("msg")` directly on the number schema |
| `Property 'fullPage' does not exist` | Wrong component used | `PageLoading` = no props; `Loading` = accepts `fullPage`, `size`, `text` |

## Tailwind v4 globals.css Template

```css
@import "tailwindcss";

@layer base {
  :root {
    --color-primary: 249 115 22;   /* orange-500 */
    /* ... */
  }
  html, body { overscroll-behavior-y: none; }  /* prevent pull-to-refresh */
  body {
    /* safe area for notched phones */
    padding-top: env(safe-area-inset-top);
    padding-bottom: env(safe-area-inset-bottom);
  }
}

@layer utilities {
  .page-container { max-width: 480px; margin-inline: auto; min-height: 100svh; }
  .scroll-area { overflow-y: auto; -webkit-overflow-scrolling: touch; }
}
```
