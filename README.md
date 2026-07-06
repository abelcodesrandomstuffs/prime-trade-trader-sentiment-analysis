# PrimeTrade AI Hiring Assignment
## Trader Performance vs Bitcoin Market Sentiment Analysis

### Overview

This project analyzes the relationship between Bitcoin market sentiment (Fear & Greed Index) and Hyperliquid trader performance.

The objective is to identify how trader behavior and profitability change under different market sentiment conditions and provide insights that could support smarter trading strategies.

---

## Dataset

### 1. Bitcoin Fear & Greed Index
Contains daily market sentiment classifications:

- Extreme Fear
- Fear
- Neutral
- Greed
- Extreme Greed

### 2. Hyperliquid Historical Trader Data

Contains historical trading information including:

- Account
- Coin
- Side (Buy/Sell)
- Direction
- Closed PnL
- Position Size
- Timestamp

---

## Project Structure

```
PrimeTrade-Assignment/

│
├── analysis_script.py
├── charts_script.py
├── historical_data.csv
├── fear_greed_index.csv
├── Trader_Sentiment_Analysis_Report.pdf
│
├── merged.parquet
├── closes.parquet
├── daily.csv
├── perf_by_bucket.csv
├── perf_by_class.csv
│
├── chart_avgpnl.png
├── chart_longshort.png
├── chart_size.png
├── chart_timeseries.png
├── chart_volume.png
├── chart_winrate.png
│
└── README.md
```

---

## Technologies Used

- Python 3
- Pandas
- NumPy
- Matplotlib

---

## Analysis Performed

The project explores:

- Trade volume across different market sentiments
- Profitability during Fear vs Greed
- Win rate comparison
- Average position sizing
- Long vs Short trading behaviour
- Coin-wise sentiment analysis
- Daily correlation between sentiment and trader performance

---

## Key Findings

- Trading activity increases during Fear markets.
- Traders tend to use larger position sizes during Fear.
- Short positions become more common during Greed.
- Highest win rates were observed during Extreme Greed and Fear.
- Different cryptocurrencies respond differently to market sentiment.

---

## Generated Outputs

Running the analysis generates:

### Intermediate Files

- merged.parquet
- closes.parquet
- daily.csv
- perf_by_bucket.csv
- perf_by_class.csv

### Visualizations

- Average PnL by Sentiment
- Trade Volume by Sentiment
- Win Rate Comparison
- Position Size Comparison
- Long vs Short Distribution
- Daily PnL Time Series

---

## How to Run

Clone the repository

```bash
git clone https://github.com/abelcodesrandomstuffs/prime-trade-trader-sentiment-analysis.git
```

Move into the project

```bash
cd prime-trade-trader-sentiment-analysis
```

Install dependencies

```bash
pip install pandas numpy matplotlib pyarrow
```

Run the analysis

```bash
python3 analysis_script.py
```

Generate charts

```bash
python3 charts_script.py
```

---

## Report

The complete analysis and findings are available in:

**Trader_Sentiment_Analysis_Report.pdf**

---

## Repository

GitHub:

https://github.com/abelcodesrandomstuffs/prime-trade-trader-sentiment-analysis

---

## Author

**Abel Koshy Alex**