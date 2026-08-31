# Reference: SatangTheBank Database Schema (Omnichannel Ledger MVP)

```sql
-- Core Ledger Table
CREATE TABLE IF NOT EXISTS transaction (
    id SERIAL PRIMARY KEY,
    org_id TEXT NOT NULL,
    transaction_type TEXT NOT NULL, -- 'INCOME' or 'EXPENSE'
    amount DOUBLE PRECISION NOT NULL,
    category TEXT NOT NULL,
    note TEXT,
    source TEXT NOT NULL, -- 'web', 'line_text', 'line_slip'
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc')
);

-- Account Binding
CREATE TABLE IF NOT EXISTS line_account (
    id SERIAL PRIMARY KEY,
    line_user_id TEXT NOT NULL UNIQUE,
    org_id TEXT NOT NULL
);
```
