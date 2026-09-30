---
name: telegram-chat-ui-ux
description: "Design rich interactive UI/UX in Telegram chat interfaces."
version: 0.1.0
metadata:
  hermes:
    tags:
      - Telegram
      - UIUX
      - Chatbot
      - Formatting
      - Interface
---

# Telegram Chat UI/UX Design

Patterns, typography rules, and interactive layouts for building production-grade mobile UI/UX inside Telegram chats. This skill covers in-place message mutation, inline keyboard matrices, expandable data cards, and callback toast flows; it does not cover external web frontend frameworks outside Telegram WebApps. Dependencies are standard Python HTTP libraries (`requests` or `httpx`).

## When to Use

- "ออกแบบ UI/UX สำหรับบอท Telegram" (Design UI/UX for a Telegram bot)
- "สร้างการ์ดพรีวิวคอนเทนต์พร้อมปุ่มกดใน Telegram" (Build content preview cards with buttons in Telegram)
- "ทำปุ่ม inline keyboard แบบอัปเดตข้อความเดิมไม่ให้รกแชท" (Build in-place updating inline keyboards without chat spam)
- "จัดฟอร์แมต Markdown/HTML สวยๆ ในแชท Telegram" (Format clean Markdown/HTML layouts in Telegram)

## Prerequisites

- Active Telegram Bot Token from `@BotFather`.
- Target Telegram `chat_id` (numeric ID or `@channel_username`).
- Python 3.10+ with `requests` installed.
- Network egress to `https://api.telegram.org`.
- Reference architecture for strict user gating and HITL state machine in `references/telegram-security-and-hitl.md`.

## How to Run

1. Format messages with strict Telegram HTML or MarkdownV2 escaping rules.
2. Render interactive cards using inline keyboard matrices via `terminal` invoking `scripts/telegram_ui_kit.py`.
3. Handle callbacks by mutating existing messages via `editMessageText` or `editMessageCaption`.

## Quick Reference

| UI Component | Method | Key Payload / Format |
| :--- | :--- | :--- |
| Preview Card | `sendMessage` / `sendPhoto` | HTML `<b>Bold</b>`, `<code>mono</code>`, `<blockquote expandable>` |
| 2D Action Matrix | `reply_markup` | `{"inline_keyboard": [[btn1, btn2], [btn3]]}` |
| In-Place Mutation | `editMessageText` | `chat_id`, `message_id`, `text`, `reply_markup` |
| Instant Toast | `answerCallbackQuery` | `callback_query_id`, `text="ข้อความแจ้งเตือน"`, `show_alert=False` |
| Mobile WebSheet | `InlineKeyboardButton` | `web_app={"url": "https://domain.com/sheet"}` |

## Procedure

1. **Construct High-Scannability Review Cards**
   Use Telegram HTML for nested tags and emoji markers. Avoid dense prose paragraphs; split information into distinct visual blocks:
   - **Header:** Status icon, category tag, and content title.
   - **Metrics Block:** Monospace tabular figures using `<code>...</code>` or `<pre>...</pre>`.
   - **Collapsible Section:** Long copy or disclaimers enclosed in `<blockquote expandable>...</blockquote>` to save vertical screen space on mobile.

2. **Assemble Inline Keyboard Matrices**
   Structure buttons into logical rows:
   - **Row 1 (Primary Actions):** Positive green action vs Neutral secondary action (`[✅ อนุมัติยิงทันที]`, `[✏️ ขอปรับแก้]`).
   - **Row 2 (Deep Dive / Links):** Web links or sub-menus (`[🖼️ เปิดภาพ Drive]`, `[📊 ดูตัวเลขดิบ]`).
   - **Row 3 (Destructive / Cancel):** Red or caution button (`[❌ ปัดตก / ยกเลิก]`).

3. **Mutate Messages In-Place (Zero Chat Spam)**
   When a user clicks a button, never send a new message into the chat. Always edit the existing message:
   - Call `editMessageCaption` or `editMessageText` with updated status.
   - Replace action buttons with a permanent status indicator (e.g. `✅ อนุมัติเรียบร้อยโดยคุณสตางค์ เมื่อ 19:35 น.`).
   - Answer the callback query within 2 seconds using `answerCallbackQuery` to dismiss the loading spinner on mobile.

4. **Surgical Multi-Step Revision Flow**
   When the user taps `[✏️ ขอปรับแก้]`, mutate the message into an inline selection sub-menu:
   - Option A: `🎣 ปรับเฉพาะท่อนเปิด (Hook)`
   - Option B: `✂️ ตัดแคปชันให้สั้นลง 30%`
   - Option C: `🎨 ปรับขนาดตัวเลขในภาพ`
   - Option D: `🎙️ พิมพ์บรีฟเอง / ส่งเสียง`
   - Include a `[🔙 ย้อนกลับ]` button to revert safely.

## Pitfalls

- **MarkdownV2 Unescaped Characters:** MarkdownV2 requires escaping 18 reserved characters (`_ * [ ] ( ) ~ \ > # + - = | { } . !`). Missing an escape on a dot (`.`) causes an instant HTTP 400 Bad Request. Prefer `parse_mode="HTML"` for automated pipelines; it only requires escaping `<`, `>`, and `&`.
- **4096-Character Limit:** A single Telegram text message is capped at 4,096 UTF-8 characters; photo captions are capped at 1,024 characters. Always truncate or use expandable blockquotes for long text.
- **Unanswered Callbacks:** Failing to invoke `answerCallbackQuery` keeps the button spinner running on mobile for up to 30 seconds, causing users to tap repeatedly.

## Verification

Test sending a styled interactive preview card to Telegram using `terminal`:
```bash
python3 scripts/telegram_ui_kit.py --dry-run
```
The script validates HTML tag nesting and prints the resolved JSON payload with inline keyboard matrix.