-- ============================================
-- Bluestock Mutual Funds Analysis
-- Day 2: SQL Analysis Queries
-- ============================================


-- 1. Total number of mutual funds
SELECT COUNT(*) AS total_funds
FROM dim_fund;


-- 2. Number of funds by category
SELECT
    category,
    COUNT(*) AS fund_count
FROM dim_fund
GROUP BY category
ORDER BY fund_count DESC;


-- 3. Number of funds by fund house
SELECT
    fund_house,
    COUNT(*) AS fund_count
FROM dim_fund
GROUP BY fund_house
ORDER BY fund_count DESC;


-- 4. Top 10 funds by 1-year return
SELECT
    scheme_name,
    return_1yr_pct
FROM fact_performance
ORDER BY return_1yr_pct DESC
LIMIT 10;


-- 5. Top 10 funds by 3-year return
SELECT
    scheme_name,
    return_3yr_pct
FROM fact_performance
ORDER BY return_3yr_pct DESC
LIMIT 10;


-- 6. Top 10 funds by 5-year return
SELECT
    scheme_name,
    return_5yr_pct
FROM fact_performance
ORDER BY return_5yr_pct DESC
LIMIT 10;


-- 7. Average 1-year return by category
SELECT
    f.category,
    ROUND(AVG(p.return_1yr_pct), 2) AS avg_return_1yr
FROM dim_fund f
JOIN fact_performance p
    ON f.amfi_code = p.amfi_code
GROUP BY f.category
ORDER BY avg_return_1yr DESC;


-- 8. Average 3-year return by category
SELECT
    f.category,
    ROUND(AVG(p.return_3yr_pct), 2) AS avg_return_3yr
FROM dim_fund f
JOIN fact_performance p
    ON f.amfi_code = p.amfi_code
GROUP BY f.category
ORDER BY avg_return_3yr DESC;


-- 9. Total investor transaction amount
SELECT
    ROUND(SUM(amount_inr), 2) AS total_transaction_amount
FROM fact_transactions;


-- 10. Transaction amount by transaction type
SELECT
    transaction_type,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_inr), 2) AS total_amount
FROM fact_transactions
GROUP BY transaction_type
ORDER BY total_amount DESC;


-- 11. Transactions by state
SELECT
    state,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_inr), 2) AS total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC
LIMIT 10;


-- 12. Transactions by age group
SELECT
    age_group,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_inr), 2) AS total_amount
FROM fact_transactions
GROUP BY age_group
ORDER BY total_amount DESC;


-- 13. AUM by fund house
SELECT
    fund_house,
    ROUND(SUM(aum_crore), 2) AS total_aum_crore
FROM fact_aum
GROUP BY fund_house
ORDER BY total_aum_crore DESC;


-- 14. Fund houses with highest number of schemes
SELECT
    fund_house,
    SUM(num_schemes) AS total_schemes
FROM fact_aum
GROUP BY fund_house
ORDER BY total_schemes DESC;


-- 15. Highest Morningstar-rated funds
SELECT
    f.scheme_name,
    p.morningstar_rating
FROM fact_performance p
JOIN dim_fund f
    ON p.amfi_code = f.amfi_code
WHERE p.morningstar_rating IS NOT NULL
ORDER BY p.morningstar_rating DESC
LIMIT 10;


-- 16. Funds with lowest expense ratio
SELECT
    f.scheme_name,
    p.expense_ratio_pct
FROM fact_performance p
JOIN dim_fund f
    ON p.amfi_code = f.amfi_code
WHERE p.expense_ratio_pct IS NOT NULL
ORDER BY p.expense_ratio_pct ASC
LIMIT 10;


-- 17. Funds with highest Sharpe ratio
SELECT
    f.scheme_name,
    p.sharpe_ratio
FROM fact_performance p
JOIN dim_fund f
    ON p.amfi_code = f.amfi_code
ORDER BY p.sharpe_ratio DESC
LIMIT 10;


-- 18. Funds with highest AUM
SELECT
    f.scheme_name,
    p.aum_crore
FROM fact_performance p
JOIN dim_fund f
    ON p.amfi_code = f.amfi_code
ORDER BY p.aum_crore DESC
LIMIT 10;


-- 19. NAV records by fund
SELECT
    amfi_code,
    COUNT(*) AS nav_records
FROM fact_nav
GROUP BY amfi_code
ORDER BY nav_records DESC;


-- 20. Check missing NAV date keys
SELECT COUNT(*) AS missing_date_keys
FROM fact_nav
WHERE date_key IS NULL;