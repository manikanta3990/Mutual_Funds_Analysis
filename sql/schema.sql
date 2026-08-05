-- ============================================
-- Bluestock Mutual Funds Analysis
-- Day 2: SQLite Star Schema
-- ============================================

PRAGMA foreign_keys = OFF;

-- ============================================
-- 1. DIMENSION: FUND
-- ============================================

DROP TABLE IF EXISTS dim_fund;

CREATE TABLE dim_fund (
    fund_key INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER NOT NULL UNIQUE,
    fund_house TEXT NOT NULL,
    scheme_name TEXT NOT NULL,
    category TEXT,
    sub_category TEXT,
    plan TEXT,
    launch_date DATE,
    benchmark TEXT,
    expense_ratio_pct REAL,
    exit_load_pct REAL,
    min_sip_amount REAL,
    min_lumpsum_amount REAL,
    fund_manager TEXT,
    risk_category TEXT,
    sebi_category_code TEXT
);

-- ============================================
-- 2. DIMENSION: DATE
-- ============================================

DROP TABLE IF EXISTS dim_date;

CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    month INTEGER NOT NULL,
    month_name TEXT NOT NULL,
    day INTEGER NOT NULL
);

-- ============================================
-- 3. FACT: NAV
-- ============================================

DROP TABLE IF EXISTS fact_nav;

CREATE TABLE fact_nav (
    nav_key INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER NOT NULL,
    date_key INTEGER NOT NULL,
    nav REAL NOT NULL,

    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code),

    FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key)
);

-- ============================================
-- 4. FACT: INVESTOR TRANSACTIONS
-- ============================================

DROP TABLE IF EXISTS fact_transactions;

CREATE TABLE fact_transactions (
    transaction_key INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id TEXT NOT NULL,
    transaction_date DATE NOT NULL,
    amfi_code INTEGER NOT NULL,
    transaction_type TEXT NOT NULL,
    amount_inr REAL NOT NULL,
    state TEXT,
    city TEXT,
    city_tier TEXT,
    age_group TEXT,
    gender TEXT,
    annual_income_lakh REAL,
    payment_mode TEXT,
    kyc_status TEXT,

    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code)
);

-- ============================================
-- 5. FACT: SCHEME PERFORMANCE
-- ============================================

DROP TABLE IF EXISTS fact_performance;

CREATE TABLE fact_performance (
    performance_key INTEGER PRIMARY KEY AUTOINCREMENT,

    amfi_code INTEGER NOT NULL,

    scheme_name TEXT,
    fund_house TEXT,
    category TEXT,
    plan TEXT,

    return_1yr_pct REAL,
    return_3yr_pct REAL,
    return_5yr_pct REAL,
    benchmark_3yr_pct REAL,

    alpha REAL,
    beta REAL,
    sharpe_ratio REAL,
    sortino_ratio REAL,

    std_dev_ann_pct REAL,
    max_drawdown_pct REAL,

    aum_crore REAL,
    expense_ratio_pct REAL,

    morningstar_rating INTEGER,
    risk_grade TEXT,

    expense_ratio_anomaly INTEGER DEFAULT 0,

    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code)
);

-- ============================================
-- 6. FACT: AUM
-- ============================================

DROP TABLE IF EXISTS fact_aum;

CREATE TABLE fact_aum (
    aum_key INTEGER PRIMARY KEY AUTOINCREMENT,
    date_key INTEGER NOT NULL,
    fund_house TEXT NOT NULL,
    aum_lakh_crore REAL,
    aum_crore REAL,
    num_schemes INTEGER,

    FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key)
);

-- ============================================
-- INDEXES
-- ============================================

CREATE INDEX idx_nav_amfi
ON fact_nav(amfi_code);

CREATE INDEX idx_nav_date
ON fact_nav(date_key);

CREATE INDEX idx_transactions_amfi
ON fact_transactions(amfi_code);

CREATE INDEX idx_transactions_date
ON fact_transactions(transaction_date);

CREATE INDEX idx_performance_amfi
ON fact_performance(amfi_code);

CREATE INDEX idx_aum_date
ON fact_aum(date_key);

-- ============================================
-- END OF SCHEMA
-- ============================================