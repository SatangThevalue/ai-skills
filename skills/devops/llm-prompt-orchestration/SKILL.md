---
name: llm-prompt-orchestration
description: "Pipeline for querying local CLIProxyAPI to generate content scripts."
version: 0.1.0
metadata:
  hermes:
    tags: [LLM, Automation, Prompt-Engineering, Local-API]
    related_skills: [content-marketing-2026-2027, thai-content-compliance]
---

# Local LLM Prompt Orchestration

This skill defines the workflow for utilizing the local `CLIProxyAPI` (running on port 42869) to generate marketing scripts, video hooks, and translated content. By keeping LLM inference local/proxied, we eliminate API costs for content generation.

## When to Use
- Generating Thai video scripts from raw product data.
- Rewriting content to fit the "5 Hook Strategies".
- Summarizing or structuring scraped data before TTS processing.

## Prerequisites
- `CLIProxyAPI` running on `http://127.0.0.1:42869`.
- Python `requests` library.

## How to Run
Invoke a Python script through the `terminal` tool that sends a crafted `messages` payload to the `/v1/chat/completions` endpoint.

## Quick Reference
- **Endpoint:** `POST http://127.0.0.1:42869/v1/chat/completions`
- **Recommended Model:** `gemini-3.5-flash-lite` (Fastest for short scripts) or `claude-sonnet-4-6` (Better for complex storytelling).

## Procedure

1. **Craft the System Prompt**
   Always inject the persona and rules into the `system` role.
   ```python
   system_prompt = """
   คุณเป็นสุดยอดนักเขียนสคริปต์วิดีโอสั้น (TikTok/Reels) สาย Affiliate
   กฎเหล็ก:
   1. ความยาวสคริปต์ไม่เกิน 45 วินาที (ประมาณ 100-120 คำ)
   2. 3 วินาทีแรกต้องเป็น Hook ที่ดึงดูดสายตา (เช่น โชว์ผลลัพธ์ หรือ พูดตัวเลขเฉพาะเจาะจง)
   3. ต้องมี "จุดบกพร่องที่สมบูรณ์แบบ" (เช่น พูดถึงข้อเสียเล็กๆ 1 ข้อ เพื่อความสมจริง)
   4. ห้ามใช้คำเคลมเกินจริง: รักษา, หายขาด, ดีที่สุดในโลก, ขาวทันที
   5. ห้ามดึงคนออกนอกแพลตฟอร์ม: ห้ามพูดคำว่า แอดไลน์, Facebook, ทักแชท
   """
   ```

2. **Execute the API Call**
   Create `scripts/llm_generator.py`:
   ```python
   import requests

   def generate_video_script(product_name, product_price):
       url = "http://127.0.0.1:42869/v1/chat/completions"
       
       user_prompt = f"เขียนสคริปต์ขายสินค้า: {product_name} (ราคา {product_price} บาท) เน้นการรีวิวแบบคนใช้งานจริง"
       
       payload = {
           "model": "gemini-3.5-flash-lite",
           "messages": [
               {"role": "system", "content": "คุณคือนักเขียนสคริปต์ TikTok Affiliate มืออาชีพ ให้เขียนแบบภาษาพูด มีเว้นจังหวะหายใจ (...) ห้ามใช้คำทางการ"},
               {"role": "user", "content": user_prompt}
           ]
       }
       
       response = requests.post(url, json=payload)
       response.raise_for_status()
       return response.json()['choices'][0]['message']['content']
   ```

3. **Validate Output**
   Pass the output of this script directly into the `thai-content-compliance` checker to ensure the LLM didn't hallucinate forbidden words.

## Pitfalls
- **Hallucinated URLs:** LLMs love to generate fake bit.ly links in scripts. Explicitly tell the LLM "ห้ามใส่ลิงก์ในสคริปต์เสียง".
- **Timeout:** If using heavy models (like 120B), the request might timeout. Set appropriate timeout limits in `requests.post(url, json=payload, timeout=60)`.
- **JSON Formatting:** If you need structured data back (e.g., returning the hook and body separately), explicitly demand `Respond ONLY in strict JSON format` and handle `json.loads()`.

## Verification
Run a test payload requesting a script about a "199 THB Powerbank". The response must be in conversational Thai without forbidden words.