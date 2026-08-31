# LINE Webhook OCR & Gemini Pipeline

When a Thai business app requires reading bank slips from LINE via an LLM, implement the following pattern:

## Requirements
- `langchain-google-genai` (or raw `httpx` to cli-proxy-api)
- `pillow` (for image processing if needed)
- `httpx` (for LINE binary downloads)

## Workflow

1. **Catch Image Events in Webhook:**
   Instead of just `type == "text"`, capture `type == "image"` from the LINE webhook.
   ```python
   elif event.get("type") == "message" and event.get("message", {}).get("type") == "image":
       message_id = event.get("message", {}).get("id")
   ```

2. **Download Binary Content from LINE:**
   LINE does not push images directly; it pushes a `message_id`. Use `httpx` to fetch the binary from `https://api-data.line.me/v2/bot/message/{message_id}/content` bearing the channel access token.

3. **Pass to Vision LLM via Base64:**
   Encode the binary as Base64 and wrap it in a LangChain `HumanMessage` or raw API call to the proxy running the Gemini-Pro Vision model.
   ```python
   # Example format for LangChain Vision
   {
       "type": "image_url",
       "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
   }
   ```

4. **Structured JSON Extraction:**
   Enforce a JSON schema via the system prompt (and model kwargs if supported) to extract:
   - `amount` (number)
   - `merchant` (string)
   - `transaction_date` (YYYY-MM-DD)
   - `transaction_time` (HH:MM)
   - `type` ("expense" / "income")

5. **Draft State Persistence:**
   Save the parsed JSON values back to the `TransactionDraft` or staging table for user confirmation, preventing hallucinated numbers from writing directly to the ledger.