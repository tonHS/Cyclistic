#!/usr/bin/env python3
"""
Cyclistic Bike-Share Case Study: Data Cleaning, Analysis & Visualization
Produces all charts and summary stats needed for the executive HTML deck.
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np
import os
import json
from pathlib import Path

# ── CONFIG ──
BASE = "/Users/admin/Desktop/Misc Fall 2024/Google course/Cyclistic Case Study using AI_2026"
RAW = os.path.join(BASE, "Raw Data ")
OUTPUT = os.path.join(BASE, "analysis_output")
os.makedirs(OUTPUT, exist_ok=True)

# Color palette
MEMBER_COLOR = "#2962A0"   # dark blue
CASUAL_COLOR = "#E67E22"   # coral/orange
COLORS = {"member": MEMBER_COLOR, "casual": CASUAL_COLOR}
BG_COLOR = "#FFFFFF"
GRID_COLOR = "#E8E8E8"

# Chart styling
plt.rcParams.update({
    'figure.facecolor': BG_COLOR,
    'axes.facecolor': BG_COLOR,
    'axes.grid': True,
    'grid.color': GRID_COLOR,
    'grid.alpha': 0.7,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'axes.labelsize': 12,
})

# ── STEP 1: LOAD DATA ──
print("=" * 60)
print("STEP 1: Loading data...")
print("=" * 60)

files = [
    os.path.join(RAW, "202501-divvy-tripdata-2_2026Feb4.csv"),  # updated Jan
    os.path.join(RAW, "202502-divvy-tripdata.csv"),
    os.path.join(RAW, "202503-divvy-tripdata.csv"),
    os.path.join(RAW, "202504-divvy-tripdata.csv"),
    os.path.join(RAW, "202505-divvy-tripdata.csv"),
    os.path.join(RAW, "202506-divvy-tripdata.csv"),
    os.path.join(RAW, "202507-divvy-tripdata.csv"),
    os.path.join(RAW, "202508-divvy-tripdata.csv"),
    os.path.join(RAW, "202509-divvy-tripdata.csv"),
    os.path.join(RAW, "202510-divvy-tripdata.csv"),
    os.path.join(RAW, "202511-divvy-tripdata.csv"),
    os.path.join(RAW, "202512-divvy-tripdata.csv"),
]

dfs = []
for f in files:
    print(f"  Loading {os.path.basename(f)}...")
    dfs.append(pd.read_csv(f, parse_dates=['started_at', 'ended_at']))

df = pd.concat(dfs, ignore_index=True)
initial_rows = len(df)
print(f"\nTotal rows loaded: {initial_rows:,}")

# ── STEP 2: CLEANING ──
print("\n" + "=" * 60)
print("STEP 2: Data cleaning...")
print("=" * 60)

cleaning_log = []
cleaning_log.append(f"Initial rows: {initial_rows:,}")

# Deduplicate
before = len(df)
df = df.drop_duplicates(subset='ride_id')
after = len(df)
dupes = before - after
cleaning_log.append(f"Duplicates removed: {dupes:,} (remaining: {after:,})")
print(f"  Duplicates removed: {dupes:,}")

# Compute ride_length in minutes
df['ride_length_min'] = (df['ended_at'] - df['started_at']).dt.total_seconds() / 60

# Remove negative/zero rides
before = len(df)
df = df[df['ride_length_min'] > 0]
after = len(df)
removed = before - after
cleaning_log.append(f"Negative/zero duration rides removed: {removed:,} (remaining: {after:,})")
print(f"  Negative/zero rides removed: {removed:,}")

# Remove rides < 1 minute
before = len(df)
df = df[df['ride_length_min'] >= 1]
after = len(df)
removed = before - after
cleaning_log.append(f"Rides < 1 minute removed: {removed:,} (remaining: {after:,})")
print(f"  Rides < 1 minute removed: {removed:,}")

# Remove rides > 24 hours (1440 minutes)
before = len(df)
df = df[df['ride_length_min'] <= 1440]
after = len(df)
removed = before - after
cleaning_log.append(f"Rides > 24 hours removed: {removed:,} (remaining: {after:,})")
print(f"  Rides > 24 hours removed: {removed:,}")

final_rows = len(df)
cleaning_log.append(f"Final clean rows: {final_rows:,}")
cleaning_log.append(f"Total rows removed: {initial_rows - final_rows:,} ({(initial_rows - final_rows) / initial_rows * 100:.1f}%)")
print(f"\n  Final clean dataset: {final_rows:,} rows")
print(f"  Total removed: {initial_rows - final_rows:,} ({(initial_rows - final_rows) / initial_rows * 100:.1f}%)")

# ── STEP 3: FEATURE ENGINEERING ──
print("\n" + "=" * 60)
print("STEP 3: Feature engineering...")
print("=" * 60)

day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
month_order = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']

df['day_of_week'] = df['started_at'].dt.day_name()
df['month'] = df['started_at'].dt.month_name()
df['month_num'] = df['started_at'].dt.month
df['hour'] = df['started_at'].dt.hour
df['is_weekend'] = df['day_of_week'].isin(['Saturday', 'Sunday'])

def get_season(m):
    if m in [12, 1, 2]:
        return 'Winter'
    elif m in [3, 4, 5]:
        return 'Spring'
    elif m in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'

df['season'] = df['month_num'].apply(get_season)
season_order = ['Winter', 'Spring', 'Summer', 'Fall']

# Check if round trip
df['is_round_trip'] = (
    df['start_station_name'].notna() &
    df['end_station_name'].notna() &
    (df['start_station_name'] == df['end_station_name'])
)

print("  Derived columns created: day_of_week, month, hour, season, is_weekend, is_round_trip")

# ── STEP 4: ANALYSIS ──
print("\n" + "=" * 60)
print("STEP 4: Analysis...")
print("=" * 60)

stats = {}

# Overall split
member_count = (df['member_casual'] == 'member').sum()
casual_count = (df['member_casual'] == 'casual').sum()
stats['total_rides'] = final_rows
stats['member_rides'] = int(member_count)
stats['casual_rides'] = int(casual_count)
stats['member_pct'] = round(member_count / final_rows * 100, 1)
stats['casual_pct'] = round(casual_count / final_rows * 100, 1)
print(f"  Members: {member_count:,} ({stats['member_pct']}%) | Casual: {casual_count:,} ({stats['casual_pct']}%)")

# Duration stats
dur = df.groupby('member_casual')['ride_length_min'].agg(['mean', 'median'])
stats['member_avg_duration'] = round(dur.loc['member', 'mean'], 1)
stats['casual_avg_duration'] = round(dur.loc['casual', 'mean'], 1)
stats['member_median_duration'] = round(dur.loc['member', 'median'], 1)
stats['casual_median_duration'] = round(dur.loc['casual', 'median'], 1)
stats['duration_ratio'] = round(stats['casual_avg_duration'] / stats['member_avg_duration'], 1)
print(f"  Avg duration - Member: {stats['member_avg_duration']} min | Casual: {stats['casual_avg_duration']} min ({stats['duration_ratio']}x)")

# Bike type
bike_type = df.groupby(['member_casual', 'rideable_type']).size().unstack(fill_value=0)
for col in bike_type.columns:
    for idx in bike_type.index:
        stats[f'{idx}_{col}_count'] = int(bike_type.loc[idx, col])
        stats[f'{idx}_{col}_pct'] = round(bike_type.loc[idx, col] / bike_type.loc[idx].sum() * 100, 1)
print(f"  Bike type analysis complete")

# Round trip
rt = df.groupby('member_casual')['is_round_trip'].mean() * 100
stats['member_round_trip_pct'] = round(rt['member'], 1)
stats['casual_round_trip_pct'] = round(rt['casual'], 1)
print(f"  Round trip % - Member: {stats['member_round_trip_pct']}% | Casual: {stats['casual_round_trip_pct']}%")

# Weekend vs weekday
weekend_data = df.groupby(['member_casual', 'is_weekend']).size().unstack(fill_value=0)
for idx in weekend_data.index:
    total = weekend_data.loc[idx].sum()
    stats[f'{idx}_weekend_pct'] = round(weekend_data.loc[idx][True] / total * 100, 1)
    stats[f'{idx}_weekday_pct'] = round(weekend_data.loc[idx][False] / total * 100, 1)
print(f"  Weekend % - Member: {stats['member_weekend_pct']}% | Casual: {stats['casual_weekend_pct']}%")

# Save stats
with open(os.path.join(OUTPUT, "stats.json"), 'w') as f:
    json.dump(stats, f, indent=2)

# Save cleaning log
with open(os.path.join(OUTPUT, "cleaning_log.txt"), 'w') as f:
    f.write("\n".join(cleaning_log))

print(f"\n  Stats and cleaning log saved.")

# ── STEP 5: VISUALIZATIONS ──
print("\n" + "=" * 60)
print("STEP 5: Generating visualizations...")
print("=" * 60)

def save_chart(fig, name):
    path = os.path.join(OUTPUT, f"{name}.png")
    fig.savefig(path, dpi=180, bbox_inches='tight', facecolor=BG_COLOR)
    plt.close(fig)
    print(f"  Saved: {name}.png")

def format_thousands(x, p):
    return f'{x:,.0f}'

# ── CHART 1: Donut chart - Overall split ──
fig, ax = plt.subplots(figsize=(7, 7))
sizes = [stats['member_rides'], stats['casual_rides']]
labels = [f"Members\n{stats['member_pct']}%", f"Casual\n{stats['casual_pct']}%"]
colors_list = [MEMBER_COLOR, CASUAL_COLOR]
wedges, texts = ax.pie(sizes, labels=labels, colors=colors_list,
                       startangle=90, wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2))
for t in texts:
    t.set_fontsize(14)
    t.set_fontweight('bold')
ax.text(0, 0, f"{final_rows / 1e6:.1f}M\nTotal Rides", ha='center', va='center',
        fontsize=16, fontweight='bold', color='#333333')
ax.set_title("Members dominate ride volume, but casuals\nrepresent a significant conversion opportunity",
             fontsize=13, fontweight='bold', pad=20)
save_chart(fig, "01_ride_volume_split")

# ── CHART 2: Monthly ride trends ──
monthly = df.groupby(['month_num', 'month', 'member_casual']).size().reset_index(name='rides')
monthly_pivot = monthly.pivot_table(index=['month_num', 'month'], columns='member_casual', values='rides', fill_value=0).reset_index()
monthly_pivot = monthly_pivot.sort_values('month_num')

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(monthly_pivot['month'], monthly_pivot['member'], color=MEMBER_COLOR,
        marker='o', linewidth=2.5, markersize=6, label='Members', zorder=3)
ax.plot(monthly_pivot['month'], monthly_pivot['casual'], color=CASUAL_COLOR,
        marker='o', linewidth=2.5, markersize=6, label='Casual', zorder=3)
ax.fill_between(range(len(monthly_pivot)), monthly_pivot['member'].values, alpha=0.08, color=MEMBER_COLOR)
ax.fill_between(range(len(monthly_pivot)), monthly_pivot['casual'].values, alpha=0.08, color=CASUAL_COLOR)
ax.set_title("Both groups peak in summer, but casual ridership\nis far more seasonal than members", fontweight='bold')
ax.set_ylabel("Number of Rides")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_thousands))
ax.legend(frameon=True, facecolor='white', edgecolor='#CCCCCC', fontsize=11)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
save_chart(fig, "02_monthly_trends")

# ── CHART 3: Day of week rides ──
dow = df.groupby(['day_of_week', 'member_casual']).size().reset_index(name='rides')
dow_pivot = dow.pivot_table(index='day_of_week', columns='member_casual', values='rides').reindex(day_order)

fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(day_order))
w = 0.35
ax.bar(x - w/2, dow_pivot['member'], w, color=MEMBER_COLOR, label='Members', zorder=3)
ax.bar(x + w/2, dow_pivot['casual'], w, color=CASUAL_COLOR, label='Casual', zorder=3)
ax.set_xticks(x)
ax.set_xticklabels(day_order, rotation=45, ha='right')
ax.set_ylabel("Number of Rides")
ax.set_title("Members ride consistently on weekdays (commuters);\ncasuals surge on weekends (leisure)", fontweight='bold')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_thousands))
ax.legend(frameon=True, facecolor='white', edgecolor='#CCCCCC', fontsize=11)
plt.tight_layout()
save_chart(fig, "03_day_of_week")

# ── CHART 4: Hourly usage ──
hourly = df.groupby(['hour', 'member_casual']).size().reset_index(name='rides')
hourly_pivot = hourly.pivot_table(index='hour', columns='member_casual', values='rides', fill_value=0)

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(hourly_pivot.index, hourly_pivot['member'], color=MEMBER_COLOR,
        linewidth=2.5, label='Members', zorder=3)
ax.plot(hourly_pivot.index, hourly_pivot['casual'], color=CASUAL_COLOR,
        linewidth=2.5, label='Casual', zorder=3)
ax.fill_between(hourly_pivot.index, hourly_pivot['member'], alpha=0.08, color=MEMBER_COLOR)
ax.fill_between(hourly_pivot.index, hourly_pivot['casual'], alpha=0.08, color=CASUAL_COLOR)
ax.axvspan(7, 9, alpha=0.06, color=MEMBER_COLOR, label='_nolegend_')
ax.axvspan(16, 18, alpha=0.06, color=MEMBER_COLOR, label='_nolegend_')
ax.set_xticks(range(0, 24))
ax.set_xticklabels([f'{h}:00' for h in range(24)], rotation=45, ha='right', fontsize=9)
ax.set_ylabel("Number of Rides")
ax.set_title("Members show clear commute peaks (8 AM, 5 PM);\ncasuals build gradually through the afternoon", fontweight='bold')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(format_thousands))
ax.legend(frameon=True, facecolor='white', edgecolor='#CCCCCC', fontsize=11)
plt.tight_layout()
save_chart(fig, "04_hourly_usage")

# ── CHART 5: Average ride duration ──
fig, ax = plt.subplots(figsize=(7, 5))
dur_data = [stats['member_avg_duration'], stats['casual_avg_duration']]
bars = ax.bar(['Members', 'Casual'], dur_data, color=[MEMBER_COLOR, CASUAL_COLOR],
              width=0.5, zorder=3, edgecolor='white', linewidth=1.5)
for bar, val in zip(bars, dur_data):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f'{val:.1f} min', ha='center', va='bottom', fontweight='bold', fontsize=13)
ax.set_ylabel("Average Ride Duration (minutes)")
ax.set_title(f"Casual riders take {stats['duration_ratio']}x longer rides on average,\nsuggesting leisure-oriented usage", fontweight='bold')
ax.set_ylim(0, max(dur_data) * 1.25)
plt.tight_layout()
save_chart(fig, "05_avg_duration")

# ── CHART 6: Duration by day of week ──
dur_dow = df.groupby(['day_of_week', 'member_casual'])['ride_length_min'].mean().reset_index()
dur_dow_pivot = dur_dow.pivot_table(index='day_of_week', columns='member_casual', values='ride_length_min').reindex(day_order)

fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(day_order))
w = 0.35
ax.bar(x - w/2, dur_dow_pivot['member'], w, color=MEMBER_COLOR, label='Members', zorder=3)
ax.bar(x + w/2, dur_dow_pivot['casual'], w, color=CASUAL_COLOR, label='Casual', zorder=3)
ax.set_xticks(x)
ax.set_xticklabels(day_order, rotation=45, ha='right')
ax.set_ylabel("Average Ride Duration (minutes)")
ax.set_title("Casual ride duration peaks on weekends;\nmember duration stays remarkably consistent", fontweight='bold')
ax.legend(frameon=True, facecolor='white', edgecolor='#CCCCCC', fontsize=11)
plt.tight_layout()
save_chart(fig, "06_duration_by_day")

# ── CHART 7: Bike type preference ──
bt = df.groupby(['member_casual', 'rideable_type']).size().reset_index(name='count')
bt_pivot = bt.pivot_table(index='member_casual', columns='rideable_type', values='count', fill_value=0)
bt_pct = bt_pivot.div(bt_pivot.sum(axis=1), axis=0) * 100

fig, ax = plt.subplots(figsize=(8, 5))
x = np.arange(len(bt_pct.index))
w = 0.35
cols = bt_pct.columns.tolist()
classic_color = '#3498DB'
electric_color = '#F39C12'
for i, col in enumerate(cols):
    c = classic_color if 'classic' in col else electric_color
    bars = ax.bar(x + i * w, bt_pct[col], w, label=col.replace('_', ' ').title(),
                  color=c, zorder=3, edgecolor='white', linewidth=1)
    for bar, val in zip(bars, bt_pct[col]):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{val:.0f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')
ax.set_xticks(x + w / 2)
ax.set_xticklabels(['Casual', 'Members'], fontsize=12)
ax.set_ylabel("Percentage of Rides")
ax.set_title("Bike type preference by rider type", fontweight='bold')
ax.set_ylim(0, 100)
ax.legend(frameon=True, facecolor='white', edgecolor='#CCCCCC', fontsize=11)
plt.tight_layout()
save_chart(fig, "07_bike_type")

# ── CHART 8: Top 10 stations for casual riders ──
casual_stations = (df[df['member_casual'] == 'casual']
                   .dropna(subset=['start_station_name'])
                   .groupby('start_station_name').size()
                   .nlargest(10)
                   .sort_values())

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(casual_stations.index, casual_stations.values, color=CASUAL_COLOR, zorder=3, height=0.6)
for bar, val in zip(bars, casual_stations.values):
    ax.text(val + casual_stations.max() * 0.01, bar.get_y() + bar.get_height()/2,
            f'{val:,}', va='center', fontsize=10)
ax.set_xlabel("Number of Rides")
ax.set_title("Top 10 start stations for casual riders\n(concentrated at tourist & lakefront locations)", fontweight='bold')
ax.xaxis.set_major_formatter(mticker.FuncFormatter(format_thousands))
plt.tight_layout()
save_chart(fig, "08_top_stations_casual")

# ── CHART 9: Top 10 stations for members ──
member_stations = (df[df['member_casual'] == 'member']
                   .dropna(subset=['start_station_name'])
                   .groupby('start_station_name').size()
                   .nlargest(10)
                   .sort_values())

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(member_stations.index, member_stations.values, color=MEMBER_COLOR, zorder=3, height=0.6)
for bar, val in zip(bars, member_stations.values):
    ax.text(val + member_stations.max() * 0.01, bar.get_y() + bar.get_height()/2,
            f'{val:,}', va='center', fontsize=10)
ax.set_xlabel("Number of Rides")
ax.set_title("Top 10 start stations for members\n(distributed across residential & business corridors)", fontweight='bold')
ax.xaxis.set_major_formatter(mticker.FuncFormatter(format_thousands))
plt.tight_layout()
save_chart(fig, "09_top_stations_member")

# ── CHART 10: Seasonal casual share ──
seasonal = df.groupby(['month_num', 'month', 'member_casual']).size().reset_index(name='rides')
seasonal_pivot = seasonal.pivot_table(index=['month_num', 'month'], columns='member_casual', values='rides', fill_value=0).reset_index()
seasonal_pivot = seasonal_pivot.sort_values('month_num')
seasonal_pivot['total'] = seasonal_pivot['member'] + seasonal_pivot['casual']
seasonal_pivot['casual_share'] = seasonal_pivot['casual'] / seasonal_pivot['total'] * 100

fig, ax = plt.subplots(figsize=(12, 6))
ax.fill_between(range(len(seasonal_pivot)), seasonal_pivot['casual_share'].values,
                alpha=0.3, color=CASUAL_COLOR, zorder=2)
ax.plot(range(len(seasonal_pivot)), seasonal_pivot['casual_share'].values,
        color=CASUAL_COLOR, linewidth=2.5, marker='o', markersize=6, zorder=3)
ax.set_xticks(range(len(seasonal_pivot)))
ax.set_xticklabels(seasonal_pivot['month'].values, rotation=45, ha='right')
ax.set_ylabel("Casual Rider Share (%)")
ax.set_title("Casual riders' share of total rides nearly doubles in summer,\nidentifying the peak conversion window", fontweight='bold')
ax.axhline(y=seasonal_pivot['casual_share'].mean(), color='#999999', linestyle='--', alpha=0.5, linewidth=1)
ax.text(11, seasonal_pivot['casual_share'].mean() + 0.5,
        f"Annual avg: {seasonal_pivot['casual_share'].mean():.0f}%",
        fontsize=10, color='#666666', ha='right')
for i, val in enumerate(seasonal_pivot['casual_share'].values):
    ax.text(i, val + 1, f'{val:.0f}%', ha='center', fontsize=9, fontweight='bold', color=CASUAL_COLOR)
ax.set_ylim(0, seasonal_pivot['casual_share'].max() + 8)
plt.tight_layout()
save_chart(fig, "10_seasonal_casual_share")

# ── CHART 11: Weekday vs Weekend split (horizontal stacked) ──
fig, ax = plt.subplots(figsize=(8, 4))
categories = ['Members', 'Casual']
weekday_vals = [stats['member_weekday_pct'], stats['casual_weekday_pct']]
weekend_vals = [stats['member_weekend_pct'], stats['casual_weekend_pct']]
y = np.arange(len(categories))
h = 0.4
ax.barh(y, weekday_vals, h, label='Weekday', color=MEMBER_COLOR, zorder=3)
ax.barh(y, weekend_vals, h, left=weekday_vals, label='Weekend', color=CASUAL_COLOR, zorder=3)
for i in range(len(categories)):
    ax.text(weekday_vals[i]/2, i, f'{weekday_vals[i]:.0f}%', ha='center', va='center',
            fontweight='bold', color='white', fontsize=12)
    ax.text(weekday_vals[i] + weekend_vals[i]/2, i, f'{weekend_vals[i]:.0f}%', ha='center', va='center',
            fontweight='bold', color='white', fontsize=12)
ax.set_yticks(y)
ax.set_yticklabels(categories, fontsize=12)
ax.set_xlabel("Percentage of Rides")
ax.set_title("Members are weekday-heavy; casuals\nshow much stronger weekend preference", fontweight='bold')
ax.legend(frameon=True, facecolor='white', edgecolor='#CCCCCC', fontsize=11)
ax.set_xlim(0, 100)
plt.tight_layout()
save_chart(fig, "11_weekday_weekend_split")

# ── Save top station names for the deck ──
stats['top_casual_stations'] = casual_stations.index.tolist()[::-1]  # descending
stats['top_member_stations'] = member_stations.index.tolist()[::-1]

# Duration by month for context
dur_month = df.groupby(['month_num', 'month', 'member_casual'])['ride_length_min'].mean().reset_index()
dur_month_pivot = dur_month.pivot_table(index=['month_num', 'month'], columns='member_casual', values='ride_length_min').reset_index().sort_values('month_num')

# Peak casual months
peak_casual_month = seasonal_pivot.loc[seasonal_pivot['casual'].idxmax(), 'month']
peak_casual_share_month = seasonal_pivot.loc[seasonal_pivot['casual_share'].idxmax(), 'month']
stats['peak_casual_month'] = peak_casual_month
stats['peak_casual_share_month'] = peak_casual_share_month
stats['peak_casual_share_val'] = round(seasonal_pivot['casual_share'].max(), 1)
stats['min_casual_share_val'] = round(seasonal_pivot['casual_share'].min(), 1)

# Resave stats with new fields
with open(os.path.join(OUTPUT, "stats.json"), 'w') as f:
    json.dump(stats, f, indent=2)

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE")
print("=" * 60)
print(f"Charts saved to: {OUTPUT}")
print(f"Stats saved to: {os.path.join(OUTPUT, 'stats.json')}")
print(f"Cleaning log saved to: {os.path.join(OUTPUT, 'cleaning_log.txt')}")
