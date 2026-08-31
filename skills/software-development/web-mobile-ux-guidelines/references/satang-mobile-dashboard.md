# Satang Mobile Dashboard Reference

This file captures the concrete mobile-dashboard conventions taught in this codebase.  
When asked to design a new mobile dashboard, reuse these tokens and patterns.

---

## 1. Layout Skeleton

```tsx
<div className="min-h-screen bg-slate-50 font-sans">
  <header className="bg-white border-b border-slate-200 sticky top-0 z-30">
    {/* Compact app bar: logo + greeting + avatar */}
  </header>

  <div className="max-w-4xl mx-auto px-4 pt-6">
    {/* Tab panels: dashboard / wallets / stats / settings */}
  </div>

  <nav className="fixed inset-x-0 bottom-0 z-40 border-t border-slate-200 bg-white/90 backdrop-blur-md">
    <div className="mx-auto max-w-lg flex justify-around">
      {/* 4 buttons, active state: text-blue-900 + show dot */}
    </div>
  </nav>
</div>
```

Rules:
- `pb-24` on root wrapper prevents content from hiding behind fixed bottom nav.
- Use `max-w-4xl mx-auto` for desktop-readable centered layout on large screens.

---

## 2. Color Tokens

```tsx
const COLORS = {
  brandDark: '#102a52',    // Logo, active nav, primary button
  brandMid: '#3b82f6',     // Secondary accents
  success: '#10b981',      // Income chips/amounts
  danger: '#f43f5e',       // Expense chips/amounts
  surface: '#f8fafc',      // Page background
  sheet: '#ffffff',        // Card bottom nav bg
  textPrimary: '#0f172a',  // Headings
  textSecondary: '#64748b',// Body copy
};
```

Tailwind aliases preferred from these values rather than random palette drift.

---

## 3. Typography

| Role | Classes |
|---|---|
| Logo / Brand | `font-extrabold text-blue-950 tracking-tight text-base` |
| Greeting | `font-bold text-[10px] text-slate-500` |
| H1 in content | `text-xl sm:text-2xl font-bold text-blue-950` |
| Money amount | `text-2xl sm:text-3xl font-extrabold` |
| Pill tag | `bg-blue-50 text-blue-700 border border-blue-100 px-2.5 py-0.5 rounded text-xs font-bold` |
| Section label | `text-[10px] font-bold uppercase tracking-wider text-slate-400` |

---

## 4. Bottom Navigation Component Pattern

```tsx
const NAV_ITEMS = [
  { key: 'dashboard', label: 'แดชบอร์ด', icon: DASHBOARD_ICON },
  { key: 'wallets', label: 'กระเป๋าเงิน', icon: WALLET_ICON },
  { key: 'stats', label: 'วิเคราะห์', icon: STATS_ICON },
  { key: 'settings', label: 'ตั้งค่า', icon: SETTINGS_ICON },
];

<nav className="fixed inset-x-0 bottom-0 z-40 border-t border-slate-200 bg-white/90 backdrop-blur-md">
  <div className="mx-auto max-w-lg flex justify-around">
    {NAV_ITEMS.map((item) => {
      const active = activeTab === item.key;
      return (
        <button
          key={item.key}
          onClick={() => setActiveTab(item.key)}
          className={`flex flex-col items-center gap-1 py-2 w-full transition-all ${active ? 'text-blue-900' : 'text-slate-400'}`}
        >
          <span className={`flex items-center justify-center rounded-2xl border transition-all ${active ? 'border-blue-900/20 bg-blue-50' : 'border-transparent'}`}>
            {item.icon}
          </span>
          <span className="text-[10px] font-extrabold tracking-wide">{item.label}</span>
          {active && <span className="h-1 w-4 rounded-full bg-blue-900 mt-0.5" />}
        </button>
      );
    })}
  </div>
</nav>
```

---

## 5. Cute Illustration System

Use lightweight stroke-based SVG icons, 24-40px, rounded caps, stroke 1.5.

```tsx
const DASHBOARD_ICON = (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#102a52" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 3 2 12h3v6h6v-4h2v4h6v-6h3L12 3zm0 7a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3z" />
  </svg>
);
```

Rules:
- Monochrome `#102a52` default.
- Optional color accent `#f59e0b` or `#10b981` on one element only.

Store reusable icons in:
`apps/frontend/src/components/dashboard/CuteIllustrations.tsx`

---

## 6. Table vs Card Responsive Rule

| Screen | Wallet/Transaction Renderer |
|---|---|
| `sm+` | Classic table row |
| `max-sm` | Stack simple cards: date / note / wallet tag / amount |

This avoids horizontal overflow on phones without losing desktop density.

---

## 7. Generic Style Pitfalls

- Never place clickable text links on the bottom nav; always use `button`.
- Keeps sticky header concise so fixed bottom nav does not skim content.
- Always update CHANGELOG / README when changing visible dashboard UX behavior.