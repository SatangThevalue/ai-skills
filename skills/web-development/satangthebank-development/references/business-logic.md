# SatangTheBank Core Features & Business Logic

## 1. Wallet Quotas
- **Free Plan**: 1 wallet (auto-provisioned as "กระเป๋าส่วนตัว", set as default).
- **Pro Plan**: 5 wallets.
- **Unlimited Plan**: 10 wallets.
*Enforcement*: 
- **Frontend**: Hides the "Create Wallet" button and shows a warning when the limit is reached. 
- **Backend API (`POST /api/wallets`)**: Blocks creation and returns a localized error `คุณถึงขีดจำกัดกระเป๋าเงินแล้ว...`. 
- **LINE Webhook**: Auto-routes transactions to the user's `is_default=True` wallet. If no wallet exists, it auto-provisions one.

## 2. UI/UX: Mobile-First Dashboard (2026 Redesign)
- **Navigation**: Fixed bottom navigation bar (Dashboard, Wallets, Stats, Settings) instead of top tabs to save vertical space and improve mobile UX. Include `pb-24` on main containers to clear the nav.
- **Design Language**: Cute illustration accents (SVG-based, stroke 1.5, monochrome `#102a52` with tiny accents like `#f59e0b` or `#10b981`).
- **Responsiveness**: Centered `max-w-4xl mx-auto` structure.
- **Empty States**: Use cute vector SVGs (e.g., smiling wallets or charts) rather than plain text.
- **Component Stack**: Uses Tailwind CSS. Header is compact (56px) with Logo and Avatar.

## 3. Pitfalls
- **Python Local Variable Scoping (UnboundLocalError)**: In monolithic files like `main.py`, do NOT use local imports (e.g., `from src.models import AiUsageLog` inside a function) if the class might be referenced in an earlier scope within the same function. Hoist these imports to the global scope at the top of the file to prevent runtime crashes.