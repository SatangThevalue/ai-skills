# LINE Loading Animation API

Using the new LINE Messaging API feature: `showLoadingAnimation`
Endpoint: `POST https://api.line.me/v2/bot/chat/loading/start`

This feature shows a blinking ellipsis (loading indicator) in the chat, similar to AI typing indicators. It is highly recommended for AI-powered chatbots where processing takes several seconds (like LLM generation or image OCR).

## SDK v3 Implementation

```python
from linebot.v3.messaging import ShowLoadingAnimationRequest

# ... inside your ApiClient context ...
with ApiClient(configuration) as api_client:
    line_bot_api = MessagingApi(api_client)
    
    # 1. Show Loading Animation (max 60 seconds)
    # chatId is the user_id (event.source.user_id)
    line_bot_api.show_loading_animation(
        ShowLoadingAnimationRequest(
            chatId=user_id, 
            loadingSeconds=30 # Specify duration (e.g., 5-60)
        )
    )
```

## Recommended Workflow for AI Chatbots
1. **Receive Webhook**: User sends a message (e.g., "Analyze this image").
2. **Immediate Loading**: Immediately fire `show_loading_animation`.
3. **Close Connection**: Return HTTP 200 OK to LINE to prevent timeout.
4. **Background Task**: Process the LLM/OCR task in a background thread or task queue (e.g., Prefect, Celery, or FastAPI `BackgroundTasks`).
5. **Final Reply**: Once the AI finishes, use the `Reply API` (if within 1 minute of the original message) or `Push API` to send the final result. The loading animation will automatically disappear when the reply arrives.
