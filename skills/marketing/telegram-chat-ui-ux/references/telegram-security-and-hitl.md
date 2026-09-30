# Telegram Security, HITL State Machine & Morning Briefing

Engineering reference for securing Telegram administration bots and executing Human-in-the-Loop (HITL) workflows.

## 1. Strict User Authorization Pattern

Never allow open, unverified execution of administrator commands. Hard-code or env-gate the authorized Telegram User ID at the router entrance:

```python
AUTHORIZED_USER_ID = 7789252439

def handle_update(update):
    user_id = update.get("from", {}).get("id")
    if user_id != AUTHORIZED_USER_ID:
        # Silently drop or return an unauthorized warning
        return
```

## 2. In-Place Mutation State Machine

To prevent message clutter, the bot mutates a single message in-place across its lifecycle:

1. **State 1: Review Card (`PENDING_REVIEW`)**
   - Displays metadata, monospace cost, expandable blockquote caption.
   - Buttons: `[ ✅ อนุมัติ ]`, `[ ✏️ ขอให้แก้ไข ]`, `[ 🖼️ ดูภาพ Drive ]`, `[ ❌ ปัดตก ]`.
2. **State 2A: Approved (`APPROVED_BY_USER`)**
   - Mutates in-place: Replaces text with a green confirmation badge and timestamp.
   - Clears action buttons to prevent duplicate taps.
3. **State 2B: Revision Sub-Menu (`REVISION_REQUESTED`)**
   - Mutates in-place: Presents 4 surgical options (`REV_HOOK`, `REV_SHORTEN`, `REV_IMAGE`, `REV_CUSTOM`).
   - Includes `[ 🔙 ยกเลิก ]` to safely restore State 1.
4. **State 2C: Rejected (`REJECTED_BY_USER`)**
   - Mutates in-place: Displays red cancellation notice and clears buttons.

## 3. Daily Executive Morning Briefing

Delivered every morning at 07:30 AM Bangkok Time (GMT+7) via Python Prefect without LLM token consumption:

- **Section 1 (Today's Plan):** Topic, pillar, template, and human-jitter scheduled time.
- **Section 2 (Queue Status):** Number of pending posts waiting for approval.
- **Section 3 (Financial & Token Ledger):** AI cost for past 24 hours and cumulative month-to-date in Thai Baht.
- **Section 4 (System Health):** Docker PostgreSQL status, Prefect server reachability, and Google Drive sync status.
