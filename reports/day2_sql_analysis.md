# Bluestock Mutual Funds Analysis

## Day 2 – SQL Database & Analysis

---

## 1. Objective

The objective of Day 2 was to create, populate, verify, and analyze a
SQLite star-schema database for the Bluestock Mutual Funds Analysis project.

The database contains information related to:

- Mutual fund schemes
- Fund houses
- Dates
- NAV history
- Investor transactions
- Scheme performance
- Assets Under Management (AUM)

---

## 2. Database Schema

A star-schema database was created using SQLite.

The following tables were created:

1. `dim_fund`
2. `dim_date`
3. `fact_nav`
4. `fact_transactions`
5. `fact_performance`
6. `fact_aum`

### Dimension Tables

- `dim_fund` – stores mutual fund scheme information.
- `dim_date` – stores date-related information such as year, quarter,
  month, and day.

### Fact Tables

- `fact_nav` – stores historical NAV records.
- `fact_transactions` – stores investor transaction information.
- `fact_performance` – stores fund performance metrics.
- `fact_aum` – stores fund-house AUM information.

---

## 3. Database Verification

The SQLite database was successfully created and populated.

### Row Count Verification

| Table | Rows |
|---|---:|
| dim_fund | 40 |
| dim_date | 1,297 |
| fact_nav | 46,000 |
| fact_transactions | 32,778 |
| fact_performance | 40 |
| fact_aum | 90 |

### Verification Result

All six main tables were successfully created and populated with data.

---

# 4. SQL Analysis

## Query 1 – Total Number of Funds

```sql
SELECT COUNT(*) AS total_funds
FROM dim_fund;