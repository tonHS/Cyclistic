# Cyclistic Bike-Share Case Study: Analysis Design Document

## 1. Business Task

**Primary Question:** How do annual members and casual riders use Cyclistic bikes differently?

**Business Objective:** Identify behavioral differences between casual riders and annual members to inform a marketing strategy aimed at converting casual riders into annual members.

**Stakeholders:** Lily Moreno (Director of Marketing), Cyclistic Marketing Analytics Team, Cyclistic Executive Team.

---

## 2. Data Source

- **Source:** Divvy/Motivate International Inc. public trip data (used as proxy for fictional Cyclistic)
- **Period:** January 2025 through December 2025 (full calendar year)
- **Volume:** ~5.55 million individual ride records across 12 monthly CSV files
- **January file:** Will use the updated file `202501-divvy-tripdata-2_2026Feb4.csv` (~138,690 rows) as it is the more complete version
- **License:** Public data, made available by Motivate International Inc.; no PII is included

### Schema (13 columns per file)

| Column | Type | Description |
|---|---|---|
| ride_id | string | Unique trip identifier |
| rideable_type | string | `classic_bike` or `electric_bike` |
| started_at | datetime | Trip start timestamp |
| ended_at | datetime | Trip end timestamp |
| start_station_name | string | Name of starting dock station (nullable) |
| start_station_id | string | ID of starting dock station (nullable) |
| end_station_name | string | Name of ending dock station (nullable) |
| end_station_id | string | ID of ending dock station (nullable) |
| start_lat | float | Starting latitude |
| start_lng | float | Starting longitude |
| end_lat | float | Ending latitude (nullable) |
| end_lng | float | Ending longitude (nullable) |
| member_casual | string | `member` or `casual` |

### Known Data Quality Issues
- **Missing station names:** ~15-22% of rows lack start/end station names (predominantly electric bike rides parked outside docks). Will analyze station-level data where available and note the gap transparently.
- **Missing end coordinates:** <0.2% of rows lack end_lat/end_lng. Will drop these for distance-related calculations.
- **Potential negative ride durations:** Some rows may have `ended_at` before `started_at` (data errors). Will filter these out.
- **Extreme ride durations:** Some rides may last days (lost/stolen bikes). Will document outlier handling.
- **Duplicate ride_ids:** Will check and deduplicate if present.

---

## 3. Data Cleaning & Preparation

### Tool Choice
**Python (pandas, matplotlib, seaborn)** — suitable for a dataset of this size (~5.5M rows), provides reproducible cleaning and publication-quality visualizations.

### Cleaning Steps
1. **Load & combine** all 12 monthly files into a single DataFrame
2. **Deduplicate** on `ride_id`
3. **Compute derived columns:**
   - `ride_length` = `ended_at` - `started_at` (in minutes)
   - `day_of_week` = day name from `started_at` (Sunday–Saturday)
   - `month` = month name from `started_at`
   - `hour` = hour of day from `started_at`
   - `season` = Winter/Spring/Summer/Fall based on month
4. **Filter invalid rides:**
   - Remove rides with `ride_length` <= 0 (bad data)
   - Remove rides with `ride_length` < 1 minute (likely false starts/redocks)
   - Remove rides with `ride_length` > 24 hours (likely lost/stolen bikes, not representative of normal usage)
5. **Document** row counts before/after cleaning

---

## 4. Analysis Plan

### Dimension 1: Ride Volume & Composition
- Total rides by member type (overall split)
- Rides by member type per month (seasonality)
- Rides by member type per day of week (weekday vs. weekend patterns)
- Rides by member type per hour of day (commute vs. leisure patterns)

### Dimension 2: Ride Duration
- Mean, median ride duration by member type
- Ride duration distribution by member type
- Mean ride duration by member type x day of week
- Mean ride duration by member type x month

### Dimension 3: Bike Type Preference
- Bike type split (classic vs. electric) by member type
- Bike type usage patterns across time dimensions

### Dimension 4: Geographic Patterns (where station data is available)
- Top 10 start stations for casual riders vs. members
- Top 10 end stations for casual riders vs. members
- Round-trip vs. one-way ride patterns (same start/end station)

### Dimension 5: Seasonal & Weather-Driven Patterns
- Month-over-month ride volume by member type
- Seasonal ride duration patterns
- How the casual/member ratio shifts across seasons

---

## 5. Planned Visualizations for Executive Deck

| Slide | Chart Type | Purpose |
|---|---|---|
| Title Slide | — | Cyclistic branding, business task, date |
| Executive Summary | Bullet points | Key findings and 3 recommendations upfront |
| Ride Volume Split | Donut/pie chart | Overall member vs. casual proportion |
| Monthly Ride Trends | Dual-line chart | Seasonality comparison, member vs. casual |
| Day-of-Week Patterns | Grouped bar chart | Weekday vs. weekend behavior differences |
| Hourly Usage | Dual-line chart | Commute peaks (members) vs. leisure spread (casual) |
| Ride Duration | Box plot or bar chart | Duration differences by member type |
| Duration by Day | Grouped bar chart | Duration x day of week x member type |
| Bike Type Preference | Stacked/grouped bar | Classic vs. electric preference by type |
| Top Stations – Casual | Horizontal bar chart | Where casuals ride most (tourism/leisure hubs) |
| Top Stations – Members | Horizontal bar chart | Where members ride most (commuter corridors) |
| Seasonal Ratio | Stacked area or line | How casual share grows in summer |
| Recommendations | Bullet points | 3 data-backed marketing recommendations |

### Visual Design Standards
- Consistent color palette: **Two primary colors** for member (e.g., dark blue) and casual (e.g., orange/coral)
- Clean white backgrounds, minimal gridlines
- Clear titles, axis labels, and data callouts on every chart
- Executive-friendly: no jargon, insight-driven chart titles (e.g., "Casual riders take 2x longer rides" rather than "Average ride length")

---

## 6. Deliverable

**Format:** Self-contained HTML presentation file with embedded charts, viewable in any browser.

**Structure:**
- ~13 slides with progressive narrative flow
- Each slide contains one key insight + one visualization
- Opens with executive summary, closes with actionable recommendations
- All charts embedded as inline images (no external dependencies)

---

## 7. Assumptions & Limitations

1. **No PII:** Cannot determine if casual riders are tourists vs. local residents
2. **No pricing data:** Cannot calculate revenue impact or price sensitivity
3. **Station gaps:** ~15-22% of rides lack station names; station-level analysis represents the docked-ride subset
4. **Single year:** Analysis covers 2025 only; year-over-year trends are not possible
5. **No weather data:** Seasonal patterns are observed but cannot be attributed to specific weather events
6. **Ride purpose is inferred:** Commute vs. leisure usage is inferred from temporal patterns, not explicit data

---

## Awaiting Approval

Please review this design document. Once approved, I will proceed with data cleaning, analysis, and deck production.
