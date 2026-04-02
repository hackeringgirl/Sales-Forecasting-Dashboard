"""
Sales Forecasting Dashboard
=============================
Uses time-series analysis to forecast future sales
and visualizes trends, seasonality, and predictions.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ── 1. GENERATE REALISTIC SALES DATA ─────────────────────────────────────────

np.random.seed(42)

# 2 years of daily sales data
dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')
n = len(dates)

# Components: trend + seasonality + noise
trend = np.linspace(10000, 18000, n)
seasonality = 3000 * np.sin(2 * np.pi * np.arange(n) / 365)
weekly_pattern = 1500 * np.sin(2 * np.pi * np.arange(n) / 7)
noise = np.random.normal(0, 800, n)

# Festival spikes (Diwali, Christmas, etc.)
festival_boost = np.zeros(n)
for i, d in enumerate(dates):
    if d.month == 10 and 20 <= d.day <= 30:  # Diwali
        festival_boost[i] = 8000
    elif d.month == 12 and 20 <= d.day <= 31:  # Christmas/New Year
        festival_boost[i] = 5000
    elif d.month == 8 and 15 <= d.day <= 20:  # Independence Day Sale
        festival_boost[i] = 3000

sales = trend + seasonality + weekly_pattern + noise + festival_boost
sales = np.maximum(sales, 0).astype(int)

df = pd.DataFrame({'date': dates, 'sales': sales})
df['month'] = df['date'].dt.month
df['weekday'] = df['date'].dt.day_name()
df['year'] = df['date'].dt.year
df.to_csv('sales_data.csv', index=False)
print("✅ Sales data created:", df.shape)

# ── 2. MONTHLY AGGREGATION ────────────────────────────────────────────────────

monthly = df.groupby(df['date'].dt.to_period('M'))['sales'].sum().reset_index()
monthly['date'] = monthly['date'].astype(str)
monthly['date'] = pd.to_datetime(monthly['date'])

# ── 3. SIMPLE MOVING AVERAGE FORECAST ────────────────────────────────────────

# Use last 3 months moving average to forecast next 3 months
window = 3
monthly['MA3'] = monthly['sales'].rolling(window=window).mean()

# Forecast next 3 months
last_date = monthly['date'].iloc[-1]
forecast_dates = [last_date + pd.DateOffset(months=i) for i in range(1, 4)]
last_ma = monthly['MA3'].dropna().iloc[-1]

# Add slight growth trend to forecast
forecast_sales = [int(last_ma * (1 + 0.02 * i)) for i in range(1, 4)]
forecast_df = pd.DataFrame({'date': forecast_dates, 'sales': forecast_sales, 'type': 'Forecast'})
monthly['type'] = 'Actual'

print("\n📈 Forecast for next 3 months:")
print(forecast_df[['date', 'sales']].to_string(index=False))

# ── 4. VISUALIZATIONS ────────────────────────────────────────────────────────

fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle('Sales Forecasting Dashboard', fontsize=18, fontweight='bold', y=1.01)

# 4a. Daily Sales Trend
axes[0, 0].plot(df['date'], df['sales'], color='#2196F3', linewidth=0.8, alpha=0.7)
axes[0, 0].fill_between(df['date'], df['sales'], alpha=0.2, color='#2196F3')
axes[0, 0].set_title('Daily Sales Trend (2023–2024)')
axes[0, 0].set_xlabel('Date')
axes[0, 0].set_ylabel('Sales (₹)')
axes[0, 0].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
axes[0, 0].tick_params(axis='x', rotation=30)

# 4b. Monthly Sales + Forecast
axes[0, 1].bar(monthly['date'], monthly['sales'], width=20, color='#4CAF50', alpha=0.8, label='Actual')
axes[0, 1].bar(forecast_df['date'], forecast_df['sales'], width=20, color='#FF9800', alpha=0.8, label='Forecast')
axes[0, 1].plot(monthly['date'], monthly['MA3'], color='red', linewidth=2, linestyle='--', label='3-Month MA')
axes[0, 1].set_title('Monthly Sales & Forecast')
axes[0, 1].set_xlabel('Month')
axes[0, 1].set_ylabel('Total Sales (₹)')
axes[0, 1].legend()
axes[0, 1].tick_params(axis='x', rotation=30)

# 4c. Sales by Day of Week
weekday_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
weekday_avg = df.groupby('weekday')['sales'].mean().reindex(weekday_order)
bars = axes[1, 0].bar(weekday_avg.index, weekday_avg.values, color='#9C27B0', alpha=0.85)
axes[1, 0].set_title('Average Sales by Day of Week')
axes[1, 0].set_xlabel('Day')
axes[1, 0].set_ylabel('Avg Sales (₹)')
axes[1, 0].tick_params(axis='x', rotation=30)
for bar, val in zip(bars, weekday_avg.values):
    axes[1, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
                    f'₹{val:,.0f}', ha='center', fontsize=7, fontweight='bold')

# 4d. Monthly Heatmap (Year x Month)
pivot = df.pivot_table(index='year', columns='month', values='sales', aggfunc='sum')
month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
pivot.columns = month_names
import seaborn as sns
sns.heatmap(pivot, annot=True, fmt=',.0f', cmap='YlOrRd', ax=axes[1, 1])
axes[1, 1].set_title('Monthly Sales Heatmap (₹)')
axes[1, 1].set_xlabel('Month')
axes[1, 1].set_ylabel('Year')

plt.tight_layout()
plt.savefig('sales_dashboard.png', dpi=150, bbox_inches='tight')
print("\n✅ Dashboard saved as sales_dashboard.png")
plt.show()

# ── 5. SUMMARY STATS ─────────────────────────────────────────────────────────

print("\n" + "="*50)
print("📋 SALES SUMMARY")
print("="*50)
print(f"Total Revenue (2024):   ₹{df[df['year']==2024]['sales'].sum():,.0f}")
print(f"Best Month:             {monthly.loc[monthly['sales'].idxmax(), 'date'].strftime('%B %Y')}")
print(f"Best Day of Week:       {weekday_avg.idxmax()}")
print(f"Avg Daily Sales:        ₹{df['sales'].mean():,.0f}")
print(f"\nForecast – Next 3 Months:")
for _, row in forecast_df.iterrows():
    print(f"  {row['date'].strftime('%B %Y')}: ₹{row['sales']:,.0f}")
