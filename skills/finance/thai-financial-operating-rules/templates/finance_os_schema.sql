-- Database Schema Template for Personal Finance OS (Double-Entry, Tax Lots, Budgets)
-- Use this template when establishing a PostgreSQL database for personal tracking.

CREATE SCHEMA IF NOT EXISTS "finance_db";

-- 1. Double-Entry Accounting Core
CREATE TABLE IF NOT EXISTS "finance_db".chart_of_accounts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    type VARCHAR(20), -- ASSET, LIABILITY, EQUITY, REVENUE, EXPENSE
    currency VARCHAR(10) DEFAULT 'THB',
    balance NUMERIC DEFAULT 0
);

-- Flat ledger for simple views (optional depending on frontend)
CREATE TABLE IF NOT EXISTS "finance_db".cashflow_ledger (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tx_type VARCHAR(10),
    category VARCHAR(50),
    amount NUMERIC,
    notes TEXT
);

-- Splits for complex tx (e.g. 1 Loan Payment = Principal + Interest)
CREATE TABLE IF NOT EXISTS "finance_db".transaction_splits (
    id SERIAL PRIMARY KEY,
    tx_id INT REFERENCES "finance_db".cashflow_ledger(id),
    account_id INT REFERENCES "finance_db".chart_of_accounts(id),
    amount NUMERIC, -- Positive = Debit, Negative = Credit
    notes TEXT
);

-- 2. Envelope Budgeting (Zero-based tracking)
CREATE TABLE IF NOT EXISTS "finance_db".budget_envelopes (
    id SERIAL PRIMARY KEY,
    month_date DATE,
    category_id VARCHAR(50),
    allocated_amount NUMERIC,
    spent_amount NUMERIC,
    rollover_amount NUMERIC
);

-- 3. Wealth & Tax Lot Tracking (FIFO basis, Crypto/Stocks)
CREATE TABLE IF NOT EXISTS "finance_db".tax_lots (
    id SERIAL PRIMARY KEY,
    asset_name VARCHAR(50),
    buy_date DATE,
    buy_price NUMERIC,
    quantity NUMERIC,
    remaining_quantity NUMERIC,
    status VARCHAR(20) DEFAULT 'OPEN' -- OPEN, CLOSED
);

-- 4. Trade Journal (Decisions and Strategy)
CREATE TABLE IF NOT EXISTS "finance_db".trade_journal (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    asset_name VARCHAR(50),
    asset_type VARCHAR(20),
    action VARCHAR(10),
    price NUMERIC,
    quantity NUMERIC,
    fees NUMERIC,
    reasoning TEXT,
    risk_assessment TEXT,
    status VARCHAR(20) DEFAULT 'OPEN'
);

-- 5. Debt Engine (Avalanche Tracking)
CREATE TABLE IF NOT EXISTS "finance_db".debt_schedule (
    id SERIAL PRIMARY KEY,
    creditor VARCHAR(50),
    interest_rate NUMERIC,
    principal_balance NUMERIC,
    monthly_payment NUMERIC,
    status VARCHAR(20) DEFAULT 'ACTIVE'
);

CREATE TABLE IF NOT EXISTS "finance_db".debt_repayment_log (
    id SERIAL PRIMARY KEY,
    debt_id INT REFERENCES "finance_db".debt_schedule(id),
    payment_date DATE DEFAULT CURRENT_DATE,
    amount_paid NUMERIC,
    principal_reduction NUMERIC,
    interest_paid NUMERIC,
    remaining_balance NUMERIC
);

-- 6. Automation Rules (Webhooks & Auto-categorization)
CREATE TABLE IF NOT EXISTS "finance_db".webhook_inbox (
    id SERIAL PRIMARY KEY,
    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    raw_payload JSONB,
    slip_amount NUMERIC,
    slip_sender VARCHAR(100),
    slip_receiver VARCHAR(100),
    processed_status BOOLEAN DEFAULT FALSE,
    linked_cashflow_id INT REFERENCES "finance_db".cashflow_ledger(id)
);

CREATE TABLE IF NOT EXISTS "finance_db".webhook_rules (
    id SERIAL PRIMARY KEY,
    sender_match VARCHAR(100), -- Regex or keyword
    auto_category VARCHAR(50),
    auto_account_id INT REFERENCES "finance_db".chart_of_accounts(id),
    is_active BOOLEAN DEFAULT TRUE
);
