"""
EV Market Analytics Dashboard — Python EDA
Project pipeline: Excel (cleaning) -> SQL (querying) -> Python (this file) -> Power BI (dashboard)

Source: ev_sales.csv (cleaned in Excel: column widths adjusted, data types
converted, duplicates/nulls checked (none found), currency verified as USD,
2026 kept as a partial/incomplete year, standardized table format)

Notes:
- No dedicated sales-region/state column exists in the dataset.
  `country_of_origin` (manufacturer's home country) is used as a proxy
  geography dimension for region-level analysis, not actual point-of-sale
  region data.
- 2026 is a partial year (~226 rows vs ~670 for 2025). Growth figures
  involving 2026 will show a misleading drop — kept in the dataset by
  decision, not corrected here.
- Several brands have gaps in year coverage (e.g. Honda: 2 of 7 years,
  Lucid/Xiaomi: 3 of 7). For those brands, YoY growth via pct_change()
  compares non-adjacent years without flagging it — only brands with a
  full 2020-2026 span (e.g. Audi, BMW, BYD, Ford, GM/Chevrolet, Hyundai,
  Kia, Rivian, Toyota, Volkswagen) have fully trustworthy YoY figures.
- price_per_range ratio was scoped out of this EDA pass.
"""

import pandas as pd

# ---------------------------------------------------------------
# 1. Load & baseline check
# ---------------------------------------------------------------
df = pd.read_csv('ev_sales.csv')

print(df.shape)
print(df.dtypes)
print(df.info())


# ---------------------------------------------------------------
# 2. YoY growth by brand
# ---------------------------------------------------------------
brand_yearly = df.groupby(['brand', 'year'])['annual_sales_units'].sum().reset_index()
brand_yearly = brand_yearly.sort_values(['brand', 'year'])
brand_yearly['yoy_growth_pct'] = brand_yearly.groupby('brand')['annual_sales_units'].pct_change() * 100

print(brand_yearly.head(20))

# Check year coverage per brand (flags brands with gaps -> unreliable YoY)
year_counts = brand_yearly.groupby('brand')['year'].count()
print(year_counts.sort_values())


# ---------------------------------------------------------------
# 3. Market share % by segment, by year
# ---------------------------------------------------------------
segment_yearly = df.groupby(['market_segment', 'year'])['annual_sales_units'].sum().reset_index()
segment_yearly['year_total'] = segment_yearly.groupby('year')['annual_sales_units'].transform('sum')
segment_yearly['market_share_pct'] = (segment_yearly['annual_sales_units'] / segment_yearly['year_total']) * 100

print(segment_yearly)


# ---------------------------------------------------------------
# 4. Correlation matrix (numeric features)
# ---------------------------------------------------------------
numeric_cols = ['price_usd', 'battery_capacity_kwh', 'range_miles', 'charging_speed_kw',
                 'acceleration_0_60_mph', 'top_speed_mph', 'horsepower', 'torque_nm',
                 'weight_kg', 'safety_rating', 'annual_sales_units', 'customer_rating']

corr_matrix = df[numeric_cols].corr()
print(corr_matrix)


# ---------------------------------------------------------------
# 5. Sales trend by body_type
# ---------------------------------------------------------------
bodytype_yearly = df.groupby(['body_type', 'year'])['annual_sales_units'].sum().reset_index()
print(bodytype_yearly)


# ---------------------------------------------------------------
# 6. Drive type distribution by year
# ---------------------------------------------------------------
drivetype_yearly = df.groupby(['drive_type', 'year'])['annual_sales_units'].sum().reset_index()
print(drivetype_yearly)


# ---------------------------------------------------------------
# 7. Autopilot level trend over time
# ---------------------------------------------------------------
autopilot_yearly = df.groupby('year')['autopilot_level'].mean().reset_index()
print(autopilot_yearly)


# ---------------------------------------------------------------
# 8. Outlier detection on price (IQR method)
# ---------------------------------------------------------------
Q1 = df['price_usd'].quantile(0.25)
Q3 = df['price_usd'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[(df['price_usd'] < lower_bound) | (df['price_usd'] > upper_bound)]
print(f"Outliers found: {len(outliers)}")
print(outliers[['brand', 'model', 'year', 'price_usd']])