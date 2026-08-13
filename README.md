# EV Market Analytics Dashboard

## Overview
This project analyzes global electric vehicle (EV) market data spanning 2020–2026, covering 20 brands and 76 brand-model combinations, to uncover trends in sales, pricing, and market composition.

## Objective
The goal was to answer: how is EV market share shifting across segments, brands, and vehicle types over time, and what does the price-to-performance tradeoff look like across the market? This project demonstrates an end-to-end analytics workflow — data cleaning, SQL querying, exploratory data analysis, and dashboard design — using Excel, SQL, Python, and Power BI together.

## Tools Used

* **Excel** — Cleaned the raw dataset: adjusted column widths, converted data types, checked for duplicates and nulls, verified currency consistency, and standardized the table format.
* **SQL (SQLite)** — Wrote grouped aggregation queries for brand-level annual sales, region-level sales (using country of origin as a geography proxy), market share by segment, top models by sales, and average price/range/ratings by brand — all by year.
* **Python (pandas, numpy)** — Ran EDA covering year-over-year growth by brand, market share percentage by segment, a correlation matrix across vehicle specs, sales trends by body type and drive type, autopilot level trends over time, and IQR-based outlier detection on price.
* **Power BI** — Built a dashboard with a title, year and category slicers, 4 KPI cards (total unit sales, total revenue, average safety rating, average customer rating), 3 donut charts (segment, drive type, body type), 2 line charts, and 2 line-and-column combo charts (including average range and battery capacity by brand).

## Dataset
2,000 rows × 24 columns, single flat table (no separate specs table required), spanning model year 2020–2026. Columns include brand, model, variant, price, battery capacity, range, charging speed, performance specs, safety and customer ratings, market segment, and annual sales units.

**Limitations to note upfront:**
- No dedicated sales-region or state column exists in the source data. `country_of_origin` (the manufacturer's home country) was repurposed as a geography proxy for regional analysis — this reflects manufacturing origin, not actual point-of-sale region.
- 2026 is a partial year (~226 rows vs. ~670 for 2025), which distorts year-over-year growth calculations for that year — this was a deliberate decision to keep the data rather than drop it.
- Several brands have incomplete year coverage (e.g. Honda: 2 of 7 years, Lucid/Xiaomi: 3 of 7), meaning YoY growth figures for those brands may span more than one calendar year.

## Process

### 1. Data Cleaning (Excel)
Adjusted column widths, converted data types to match each field (numeric, integer, text), checked for and confirmed zero duplicate rows and zero nulls, verified currency was consistent (USD) throughout, and standardized the dataset into a clean table format. The incomplete 2026 data was intentionally kept rather than excluded.

### 2. SQL Analysis
Queried the cleaned dataset in SQLite to compute: brand-level annual sales by year, region-level sales by year (using country of origin), market share by segment by year, top-selling models by year, and average price/range/customer/safety ratings by brand and year. Full query file: `queries.sql`.

### 3. Python EDA
Used pandas to calculate year-over-year growth by brand (`pct_change()`), market share percentage by segment (`groupby` + `transform`), a correlation matrix across numeric vehicle specs, sales trends broken out by body type and drive type, average autopilot level by year, and IQR-based outlier detection on price. Full script: `ev_sales.py`.

### 4. Power BI Dashboard
*(Insert dashboard screenshot here)*

The dashboard includes a title, year and category slicers, 4 KPI cards (total unit sales, total revenue, average safety rating, average customer rating), 3 donut charts (market segment, drive type, body type composition), 2 line charts (yearly total sales trend), and 2 line-and-column combo charts (including average range and battery capacity by brand).

## Key Findings

* Premium and Mid-range segments have consistently led the market, together accounting for roughly 60-70% of annual sales share every year from 2020-2026, while Budget-segment share has steadily declined (from ~14.6% in 2020 to ~5.8% in 2026 YTD).
* Sales growth was strongest among newer/scaling entrants like BYD and Audi in the early-to-mid dataset years (BYD: +184% in 2021, Audi: +152% in 2022), while established full-span brands (BMW, Toyota, Volkswagen) show steadier, more moderate YoY growth.
* Several brands (Honda, Lucid, Xiaomi, Polestar, Volvo, NIO) have incomplete year coverage in the dataset, which limits how directly their growth can be compared to full-span brands like Tesla or Ford.
* 2026 figures are partial-year data and should be read as YTD, not a full-year comparison — most brands show a sharp apparent drop in 2026 that reflects incomplete data collection, not an actual market decline.
* Geography in this analysis reflects manufacturer origin (`country_of_origin`), not actual sales region — a limitation of the source dataset that should be considered when interpreting the map visual.

## Files in This Repo

* `ev market analysis raw.csv` — raw dataset
* `ev_sales.csv` — cleaned dataset
* `queries.sql` — all SQL queries
* `ev_sales.py` — Python EDA script
* `ev market analytics dashboard.pbix` — Power BI dashboard export

## What I Learned

This project reinforced how much a dataset's structural gaps — missing years for certain brands, no true sales-region field, a partial final year — shape which analyses are actually trustworthy, not just which ones are technically possible to run. Working through the SQL GROUP BY/aggregation-grain issues also sharpened my understanding of why non-aggregated columns in a SELECT can silently return misleading values depending on the SQL engine, even without throwing an error.
