# LINE Bot AI Loading Animation Pattern

When integrating long-running AI tasks (e.g., LLM text generation, OCR on slips) via LINE Webhook, you must return an HTTP 200 OK within 1-2 seconds to prevent LINE from marking the webhook as failed (Time-out).

To provide excellent UX (showing the user that the AI is "thinking") and avoid burning Push Message quotas unnecessarily, use the `showLoadingAnimation` API combined with FastAPI `BackgroundTasks`.

## Optimal Workflow:
1. **Receive Webhook**: Validate signature in the main endpoint.
2. **Start Background Task**: Dispatch the AI processing function via `background_tasks.add_task(...)`.
3. **Return HTTP 200 OK**: Immediately close the connection with LINE so it doesn't time out.
4. **Background Task Execution**:
   - **Show Loading**: Call `show_loading_animation(chatId=user_id, loadingSeconds=30)`. This displays the "..." typing indicator in the user's chat.
   - **Process AI**: Run the long-running task (e.g., LangChain processing, database save).
   - **Reply**: Once done, use the original `reply_token` (valid for up to 1 minute) to send the final result (e.g., a Flex Message). Sending a reply automatically clears the loading animation.

## Code Implementation Example
```python
from fastapi import BackgroundTasks
from linebot.v3.messaging import ShowLoadingAnimationRequest, ReplyMessageRequest, FlexMessage

@app.post("/webhooks/line")
async def line_webhook(request: Request, background_tasks: BackgroundTasks):
    # ... signature validation ...
    
    # Dispatch to background task
    background_tasks.add_task(process_ai, event.reply_token, event.source.user_id, event.message.text)
    
    # Immediately return 200 OK
    return {"status": "ok"}

async def process_ai(reply_token: str, user_id: str, text: str):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        # 1. Show Loading Animation (e.g., 30s)
        try:
            line_bot_api.show_loading_animation(
                ShowLoadingAnimationRequest(chatId=user_id, loadingSeconds=30)
            )
        except Exception as e:
            print(f"Loading Animation Error: {e}")

        # 2. Long running task (AI Processing, DB Saving)
        await asyncio.sleep(5) 
        
        # 3. Reply with result (clears the loading animation)
        try:
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=reply_token,
                    messages=[...] # Your TextMessage or FlexMessage
                )
            )
        except Exception as e:
            print(f"Reply Error: {e}")
```
