---
name: finance-os-tracker
description: Process daily financial transactions and route them to FinanceOS double-entry system via MCP tools.
---

# Finance OS Tracker

## When to Use
Use this skill when the user reports spending, receiving money, investing, or moving funds (e.g., "กินข้าว 150", "เงินเดือนเข้า", "ซื้อหุ้น").

## Account Categories (Strict)
You must map all user inputs to these exact account names. Do not invent new ones.

**Assets (แหล่งเงิน):**
- `ACC_MAIN` (บัญชีใช้จ่ายหลัก)
- `ACC_EMERGENCY` (เงินสำรอง)
- `ACC_TH_STOCK`, `ACC_US_STOCK`, `ACC_CRYPTO`, `ACC_TAX_FUND` (พอร์ตลงทุน)

**Liabilities (หนี้):**
- `LIA_CREDIT_CARD` (บัตรเครดิต)
- `LIA_PERSONAL_LOAN` (สินเชื่อส่วนบุคคล)

**Income (รายรับ - Source):**
- `INC_SALARY`, `INC_GIG`, `INC_DIVIDEND`, `INC_INTEREST`

**Expenses (รายจ่าย - Destination):**
- `EXP_HOUSING`, `EXP_FOOD`, `EXP_TRANSPORT`, `EXP_DINE_OUT`, `EXP_ENTERTAIN`, `EXP_SHOPPING`
- `EXP_DEBT_MIN` (จ่ายหนี้ขั้นต่ำ), `EXP_DEBT_EXTRA` (โปะหนี้)

## Rules & Execution
1. Every transaction is Double-Entry. It must have a source and a destination.
2. Call the MCP tool: `log_transaction(src_acct, dest_acct, amount, notes)`.
3. Do not ask for confirmation if the intent is clear. Just log it and confirm success.

### Mapping Examples
- **Spending Cash:** User "ซื้อกาแฟ 80" -> `log_transaction(src_acct='ACC_MAIN', dest_acct='EXP_DINE_OUT', amount=80, notes='กาแฟ')`
- **Earning Money:** User "ได้ค่าจ้าง 5000" -> `log_transaction(src_acct='INC_GIG', dest_acct='ACC_MAIN', amount=5000, notes='ค่าจ้าง')`
- **Investing:** User "โอนเงินไปซื้อหุ้นไทย 2000" -> `log_transaction(src_acct='ACC_MAIN', dest_acct='ACC_TH_STOCK', amount=2000, notes='เติมพอร์ตหุ้นไทย')`
- **Paying Credit Card:** User "จ่ายบัตรเครดิต 3000" -> `log_transaction(src_acct='ACC_MAIN', dest_acct='LIA_CREDIT_CARD', amount=3000, notes='จ่ายบัตร')`

## Portfolio Checks
- If the user asks "มีเงินเท่าไหร่" or "สรุปพอร์ต", call `get_account_balances()` or `get_net_worth()` and present the data clearly.

## System Architecture & Technical Patterns
- **Database Structure:** See `references/schema_ddl.sql` for the complete `finance_db` PostgreSQL schema (Chart of Accounts, Trading Universe, Paper Trade Logs, Webhook Inbox).
- **Quant Engine Workflow:** Uses Prefect with `ThreadPoolTaskRunner` for concurrent execution, checking market hours via Python's `zoneinfo` (e.g. `Asia/Bangkok` for TH assets, `UTC` for Crypto) before triggering model evaluation.
- **Data Ingestion Pattern:** Uses a Hybrid approach (query 100 historical candles from DB + 1 live tick from API) to drastically reduce broker API rate limits.
- **FastMCP + FastAPI Integration Pitfall:** FastMCP (v4.0.5+) mounts to an existing FastAPI app using `mcp.mount(app)`. **Do not** attempt to use `app.mount("/mcp", mcp.asgi_app)` or `mcp.get_starlette_app()` as they result in `AttributeError`.