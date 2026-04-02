# 📈 Sales Forecasting Dashboard

A time-series analytics project that forecasts future sales using Moving Average techniques and visualizes sales trends, seasonality, and festival impacts.

## 📌 Project Overview

Sales forecasting helps businesses plan inventory, staffing, and marketing budgets. This project analyzes 2 years of daily sales data and predicts the next 3 months.

## 🧠 What I Built

- Generated 2 years (730 days) of realistic sales data with trend, seasonality, weekly patterns, and festival boosts (Diwali, Christmas, Independence Day)
- Applied 3-Month Moving Average (MA3) for smoothing and forecasting
- Built a 4-panel interactive dashboard

## 📊 Key Insights

- October (Diwali) consistently shows the highest sales spike
- Weekend sales are ~15% higher than weekday sales
- Year-over-year growth trend of approximately 8%
- Forecast for Q1 2025 shows continued upward trajectory

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Pandas | Time-series manipulation |
| NumPy | Data generation & math |
| Matplotlib | Multi-panel dashboard |
| Seaborn | Heatmap visualization |

## 📁 Files

```
03-sales-forecasting/
├── sales_forecasting.py     # Main forecasting script
├── sales_data.csv           # Generated daily sales data
├── sales_dashboard.png      # Visual dashboard output
└── README.md
```

## 🚀 How to Run

```bash
pip install pandas numpy matplotlib seaborn
python sales_forecasting.py
```

## 🔮 Forecasting Method

Used **Moving Average (MA3)** — a simple but effective baseline method:
- Averages the last 3 months of sales
- Applies a 2% monthly growth factor for trend adjustment
- Suitable for stable time series with clear patterns

## 👩‍💻 Author

**hackeringgirl** — Built as part of my Data Analytics & Cybersecurity portfolio
