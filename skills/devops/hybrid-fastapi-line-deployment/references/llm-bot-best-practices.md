# LLM Line Bot Best Practices

## 1. Concurrency and Rate Limiting
- **Don't block the Webhook**: LINE requires webhooks to return HTTP 200 within a few seconds. When using LLMs (which take 2-10 seconds per call), you *must* offload the processing. In FastAPI, pass the events to `BackgroundTasks` and return `{"status": "ok"}` immediately.
- **Batch Processing**: Users often upload 5-10 images at once. A background task must process these concurrently (e.g., using `asyncio.gather`) or quickly enough sequentially so the `replyToken` doesn't expire.

## 2. Cost Optimization (Reply vs Push)
- LINE's `PushMessage` API consumes your monthly quota (1,000 free messages).
- `ReplyMessage` is 100% free and unlimited, but the `replyToken` is only valid for 1 minute and can only be used once.
- **Strategy**: Accumulate the LLM results in the background task. As long as the total processing time is under 1 minute, construct a single Flex Message with multiple bubbles (or a combined text message) and send it using the *latest* `replyToken` from that batch of events. Avoid Push API unless absolutely necessary for delayed notifications.

## 3. UX: Loading Animations
- Since LLMs take time, users might think the bot is broken.
- Use LINE's `show_loading_animation` (available in Messaging API SDK v3).
- **Implementation**: Call `show_loading_animation(chatId=user_id, loadingSeconds=40)` *before* starting the LLM call. The animation automatically disappears when you send the final reply.

## 4. Prompt Engineering for Databases
- Do not let the LLM invent categories. It will fragment your database (e.g., "กาแฟ", "เครื่องดื่ม", "Coffee").
- **Solution**: Hardcode a `ALLOWED_CATEGORIES` list in Python, inject it into the prompt (`"Category MUST be exactly one of: [list]"`), and implement a Python fallback (`if result['category'] not in ALLOWED_CATEGORIES: result['category'] = 'Other'`).

## 5. Telemetry
- Always extract the `usage` object from the LLM response (`prompt_tokens`, `completion_tokens`).
- Log this alongside the `latency_ms` to a database table (e.g., `ai_usage_log`) to track costs and identify slow prompts over time.