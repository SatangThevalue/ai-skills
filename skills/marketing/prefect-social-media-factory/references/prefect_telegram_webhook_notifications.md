# Prefect v3 Custom Webhook Notifications for Telegram

Guide for configuring, saving, and invoking Telegram alerts through Prefect's native notification framework without writing custom HTTP requests inside every task.

## 1. Overview & Architecture

Prefect 3 provides `CustomWebhookNotificationBlock` to route alerts to external endpoints using Jinja-like template placeholders:
- `{{ subject }}`: High-level notification headline
- `{{ body }}`: Detailed message payload or stack trace

When saved to a dedicated Prefect Server, any worker or flow can load the block by name and trigger real-time Telegram alerts on flow completion or failure.

## 2. Configuration & Saving the Block

Execute from Python environment with active `PREFECT_API_URL`:

```python
from prefect.blocks.notifications import CustomWebhookNotificationBlock

bot_token = "YOUR_TELEGRAM_BOT_TOKEN"
chat_id = "7789252439"

telegram_block = CustomWebhookNotificationBlock(
    name="telegram-satang-alerts",
    url=f"https://api.telegram.org/bot{bot_token}/sendMessage",
    method="POST",
    json_data={
        "chat_id": chat_id,
        "text": "🔔 *[Prefect Alert]* {{ subject }}\n\n{{ body }}",
        "parse_mode": "Markdown",
    },
)

telegram_block.save("telegram-satang-alerts", overwrite=True)
```

## 3. Flow State Change Hooks

Attach failure or completion alerts directly to `@flow` decorators:

```python
from prefect import flow
from prefect.blocks.notifications import CustomWebhookNotificationBlock

def on_flow_failure_hook(flow, flow_run, state):
    block = CustomWebhookNotificationBlock.load("telegram-satang-alerts")
    block.notify(
        subject=f"🚨 Flow Failed: {flow.name}",
        body=f"Flow run '{flow_run.name}' failed with state: {state.name}\nMessage: {state.message}"
    )

@flow(name="Scheduled Worker Flow", on_failure=[on_flow_failure_hook])
def my_production_flow():
    # flow execution logic
    pass
```

## 4. Key Server Settings & Version Compatibility

- **Major Version Alignment:** Ensure both the client and server container run the same major version (e.g. Prefect 3.x). Mismatches trigger `RuntimeError: Found incompatible versions: client: 3.x, server: 2.x`.
- **Server Flags for Triggers:** For Prefect server to run event-driven automations, ensure `PREFECT_EXPERIMENTAL_EVENTS=true` and `PREFECT_API_SERVICES_TRIGGERS_ENABLED=true` are active in the server container environment.
