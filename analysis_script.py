import pandas as pd
import numpy as np

pd.set_option('display.width', 140)

# ---------- Load ----------
fg = pd.read_csv('/mnt/user-data/uploads/fear_greed_index.csv')
hd = pd.read_csv('/mnt/user-data/uploads/historical_data.csv')

fg['date'] = pd.to_datetime(fg['date'])
hd['Timestamp IST'] = pd.to_datetime(hd['Timestamp IST'], format='%d-%m-%Y %H:%M')
hd['date'] = hd['Timestamp IST'].dt.normalize()

# ---------- Merge ----------
df = hd.merge(fg[['date', 'classification', 'value']], on='date', how='left')
print("Unmatched dates:", df['classification'].isna().sum(), "of", len(df))

# Collapse 5-class sentiment into simple Fear/Greed/Neutral bucket for headline comparisons
def bucket(c):
    if pd.isna(c): return np.nan
    if 'Fear' in c: return 'Fear'
    if 'Greed' in c: return 'Greed'
    return 'Neutral'
df['sentiment_bucket'] = df['classification'].apply(bucket)

# Only trades that actually realize PnL (closing trades) matter for performance analysis
closes = df[df['Closed PnL'] != 0].copy()
closes['win'] = closes['Closed PnL'] > 0
closes['abs_size'] = closes['Size USD']

print("\n=== Trade counts by sentiment (all trades) ===")
print(df['classification'].value_counts())

print("\n=== Overall performance by 5-class sentiment (closing trades only) ===")
perf = closes.groupby('classification').agg(
    trades=('Closed PnL', 'count'),
    total_pnl=('Closed PnL', 'sum'),
    avg_pnl=('Closed PnL', 'mean'),
    median_pnl=('Closed PnL', 'median'),
    win_rate=('win', 'mean'),
    avg_size_usd=('abs_size', 'mean'),
).round(3)
print(perf)

print("\n=== Overall performance by bucket (Fear/Greed/Neutral) ===")
perf_b = closes.groupby('sentiment_bucket').agg(
    trades=('Closed PnL', 'count'),
    total_pnl=('Closed PnL', 'sum'),
    avg_pnl=('Closed PnL', 'mean'),
    median_pnl=('Closed PnL', 'median'),
    win_rate=('win', 'mean'),
    avg_size_usd=('abs_size', 'mean'),
).round(3)
print(perf_b)

# ---------- Leverage / risk proxy: position size relative to account activity ----------
print("\n=== Avg trade size (USD) by sentiment ===")
print(df.groupby('classification')['Size USD'].mean().round(2))

# ---------- Long vs Short behavior by sentiment ----------
print("\n=== Direction mix by sentiment (share of trades) ===")
dir_mix = pd.crosstab(df['classification'], df['Side'], normalize='index').round(3)
print(dir_mix)

open_trades = df[df['Direction'].isin(['Open Long','Open Short'])]
print("\n=== Open Long vs Open Short share by sentiment ===")
open_mix = pd.crosstab(open_trades['classification'], open_trades['Direction'], normalize='index').round(3)
print(open_mix)

# ---------- Per-account performance under each sentiment ----------
acct_sent = closes.groupby(['Account','sentiment_bucket'])['Closed PnL'].sum().unstack(fill_value=0)
print("\n=== Number of accounts profitable overall ===")
acct_total = closes.groupby('Account')['Closed PnL'].sum().sort_values(ascending=False)
print("Profitable accounts:", (acct_total>0).sum(), "/ Total:", len(acct_total))

# ---------- Top coins traded and their PnL by sentiment ----------
print("\n=== Top 10 coins by trade volume ===")
print(df['Coin'].value_counts().head(10))

top_coins = df['Coin'].value_counts().head(5).index.tolist()
print("\n=== Avg PnL by sentiment for top 5 coins ===")
coin_sent = closes[closes['Coin'].isin(top_coins)].groupby(['Coin','sentiment_bucket'])['Closed PnL'].mean().unstack().round(2)
print(coin_sent)

# ---------- Daily aggregation for trend / correlation ----------
daily = df.groupby('date').agg(
    daily_pnl=('Closed PnL','sum'),
    trades=('Closed PnL','size'),
    avg_size=('Size USD','mean'),
).reset_index()
daily = daily.merge(fg[['date','value','classification']], on='date', how='left')
corr = daily[['daily_pnl','value']].corr().iloc[0,1]
print("\nCorrelation between daily PnL and Fear/Greed numeric value:", round(corr,4))

corr_trades = daily[['trades','value']].corr().iloc[0,1]
print("Correlation between daily trade count and Fear/Greed numeric value:", round(corr_trades,4))

corr_size = daily[['avg_size','value']].corr().iloc[0,1]
print("Correlation between avg trade size and Fear/Greed numeric value:", round(corr_size,4))

# Save intermediate outputs for chart-building
df.to_parquet('/home/claude/analysis/merged.parquet')
daily.to_csv('/home/claude/analysis/daily.csv', index=False)
closes.to_parquet('/home/claude/analysis/closes.parquet')
perf.to_csv('/home/claude/analysis/perf_by_class.csv')
perf_b.to_csv('/home/claude/analysis/perf_by_bucket.csv')
print("\nSaved intermediate files.")
