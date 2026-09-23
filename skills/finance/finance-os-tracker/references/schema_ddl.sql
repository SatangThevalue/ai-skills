CREATE SCHEMA IF NOT EXISTS "finance_db";

-- 1. Double-Entry Accounting Core
CREATE TABLE IF NOT EXISTS "finance_db".chart_of_accounts (
    id SERIAL PRIMARY KEY, 
    name VARCHAR(100), 
    type VARCHAR(20), 
    currency VARCHAR(10) DEFAULT 'THB', 
    balance NUMERIC DEFAULT 0
);

CREATE TABLE IF NOT EXISTS "finance_db".cashflow_ledger (
    id SERIAL PRIMARY KEY, 
    tx_type VARCHAR(10), 
    category VARCHAR(50), 
    amount NUMERIC, 
    notes TEXT, 
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "finance_db".transaction_splits (
    id SERIAL PRIMARY KEY, 
    tx_id INT, 
    account_id INT, 
    amount NUMERIC, 
    notes TEXT
);

-- 2. Webhook Inbox (LINE/Telegram Data)
CREATE TABLE IF NOT EXISTS "finance_db".webhook_inbox (
    id SERIAL PRIMARY KEY, 
    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    raw_payload JSONB, 
    processed_status BOOLEAN DEFAULT FALSE
);

-- 3. Portfolios & Limits
CREATE TABLE IF NOT EXISTS "finance_db".portfolio_status (
    id SERIAL PRIMARY KEY, 
    total_capital NUMERIC, 
    emergency_fund NUMERIC, 
    high_interest_debt NUMERIC, 
    risk_level VARCHAR(20), 
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);

-- 4. Quant Trading Engine
CREATE TABLE IF NOT EXISTS "finance_db".trading_universe (
    id SERIAL PRIMARY KEY, 
    asset_name VARCHAR(50) UNIQUE, 
    asset_type VARCHAR(20), 
    timezone VARCHAR(50), 
    market_open TIME, 
    market_close TIME, 
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS "finance_db".market_data (
    id SERIAL PRIMARY KEY, 
    asset_name VARCHAR(50), 
    timeframe VARCHAR(10), 
    timestamp TIMESTAMP, 
    open NUMERIC, 
    high NUMERIC, 
    low NUMERIC, 
    close NUMERIC, 
    volume NUMERIC, 
    UNIQUE(asset_name, timeframe, timestamp)
);

CREATE TABLE IF NOT EXISTS "finance_db".model_registry (
    id SERIAL PRIMARY KEY, 
    version_tag VARCHAR(50), 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    weight_pa NUMERIC, 
    weight_ind NUMERIC, 
    weight_vol NUMERIC, 
    weight_ml NUMERIC, 
    lgb_learning_rate NUMERIC, 
    lgb_max_depth INT, 
    execution_threshold NUMERIC, 
    backtest_winrate NUMERIC, 
    is_active BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS "finance_db".paper_trade_log (
    id SERIAL PRIMARY KEY, 
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    asset_name VARCHAR(50), 
    entry_price NUMERIC, 
    sl_price NUMERIC, 
    tp_price NUMERIC, 
    pa_score NUMERIC, 
    ind_score NUMERIC, 
    vol_score NUMERIC, 
    ml_score NUMERIC, 
    regime_multiplier NUMERIC, 
    final_score NUMERIC, 
    simulated_pnl NUMERIC DEFAULT 0, 
    status VARCHAR(20) DEFAULT 'OPEN'
);
