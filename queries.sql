/* ============================================================
   EV Market Analytics Dashboard — SQL Queries
   Project: EV (Electric Vehicle) Market Analytics Dashboard
   Pipeline: Excel (cleaning) -> SQL (this file) -> Python (EDA) -> Power BI (dashboard)

   Source table: ev_sales
   (Loaded from ev_market_analysis_raw.csv after Excel cleaning:
    column widths adjusted, data types converted, duplicates/nulls
    checked (none found), currency verified as USD, 2026 data kept
    as partial-year, standardized table format)

   Notes on the dataset:
   - Single flat table, no separate specs table -> no joins required
   - No dedicated sales-region/state column exists. `country_of_origin`
     (manufacturer's home country) is repurposed as the geography
     dimension for region-level analysis and the Power BI map.
     This is a proxy for regional market presence, NOT actual
     point-of-sale region data — flagged here for documentation.
   - year range: 2020-2026 (2026 is a partial/incomplete year, kept
     in the dataset by decision, but should be treated as YTD when
     computing growth rates downstream in Python).
   - LAG()/window-function based YoY growth was intentionally skipped
     at the SQL stage — deferred to the Python step for EDA.
   ============================================================ */


/* ------------------------------------------------------------
   Query 1: Brand-level annual sales by year
   Purpose: base aggregate table for brand performance over time
   ------------------------------------------------------------ */
select
    brand,
    year,
    sum(annual_sales_units) as total_sales
from ev_sales
group by brand, year;


/* ------------------------------------------------------------
   Query 2: Region-level sales by year
   Purpose: feeds the Power BI geographic adoption map, paired
   with the time-series adoption growth line.
   Geography proxy: country_of_origin
   ------------------------------------------------------------ */
select
    country_of_origin,
    year,
    sum(annual_sales_units) as total_sales
from ev_sales
group by country_of_origin, year;


/* ------------------------------------------------------------
   Query 3: Market share by segment, by year
   Purpose: raw segment sales totals per year. Percentage-of-total
   share calculation deferred to the Python step rather than
   computed here with a window function.
   ------------------------------------------------------------ */
select
    market_segment,
    year,
    sum(annual_sales_units) as total_sales
from ev_sales
group by market_segment, year;


/* ------------------------------------------------------------
   Query 4: Top models by sales, by year
   Purpose: model-level ranking input for Power BI table/ranking
   visual. Sorted (not row-limited) per year since per-year TOP-N
   via ROW_NUMBER()/PARTITION BY was intentionally kept out of
   scope at this stage.
   ------------------------------------------------------------ */
select
    model,
    year,
    sum(annual_sales_units) as total_sales
from ev_sales
group by model, year
order by year, total_sales desc;


/* ------------------------------------------------------------
   Query 5: Average price and range by brand, by year
   Purpose: context for the price-per-range ratio calculated in
   the Python step, and for brand-level comparison in Excel/Power BI.

   Note: `model` was intentionally left out of SELECT/GROUP BY here
   since this query is scoped to brand-year grain. Including `model`
   without adding it to GROUP BY would return an arbitrary per-group
   value for that column in SQLite/MySQL (no error thrown, but not
   a meaningful value) — avoided by excluding it.
   If model-level granularity is needed later (e.g. for the
   price-vs-range scatter plot), rerun with:
       group by brand, model, year
   and add `model` back into the SELECT list.
   ------------------------------------------------------------ */
select
    brand,
    year,
    round(avg(price_usd), 1) as avg_price,
    round(avg(range_miles), 1) as avg_range
from ev_sales
group by brand, year;


/* ------------------------------------------------------------
   Query 6: Average customer and safety rating by brand, by year
   Purpose: supporting metrics for a Power BI comparison card/table.

   Note: same `model` grain consideration as Query 5 applies —
   left out of SELECT/GROUP BY since this is brand-year grain.
   ------------------------------------------------------------ */
select
    brand,
    year,
    round(avg(customer_rating), 1) as avg_rating,
    round(avg(safety_rating), 1) as avg_safety
from ev_sales
group by brand, year;
