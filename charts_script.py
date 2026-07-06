import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

plt.rcParams.update({
    'font.size': 11,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
})

COLORS = {
    'Extreme Fear': '#8B0000',
    'Fear': '#E76F51',
    'Neutral': '#A8A8A8',
    'Greed': '#2A9D8F',
    'Extreme Greed': '#1B4332',
}
ORDER = ['Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed']

df = pd.read_parquet('merged.parquet')
closes = pd.read_parquet('closes.parquet')
daily = pd.read_csv('daily.csv', parse_dates=['date'])

# 1. Win rate by sentiment class
perf = closes.groupby('classification').agg(win_rate=('win','mean'), avg_pnl=('Closed PnL','mean'), trades=('Closed PnL','count'))
perf = perf.reindex(ORDER)

fig, ax = plt.subplots(figsize=(8,5))
bars = ax.bar(perf.index, perf['win_rate']*100, color=[COLORS[c] for c in perf.index])
ax.set_ylabel('Win Rate (%)')
ax.set_title('Trader Win Rate by Market Sentiment', fontsize=13, fontweight='bold')
ax.set_ylim(0, 100)
for b, v in zip(bars, perf['win_rate']*100):
    ax.text(b.get_x()+b.get_width()/2, v+1.5, f'{v:.1f}%', ha='center', fontsize=10)
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig('chart_winrate.png', dpi=150)
plt.close()

# 2. Average PnL per closing trade by sentiment
fig, ax = plt.subplots(figsize=(8,5))
bars = ax.bar(perf.index, perf['avg_pnl'], color=[COLORS[c] for c in perf.index])
ax.set_ylabel('Average Closed PnL (USD)')
ax.set_title('Average Profit per Closing Trade by Market Sentiment', fontsize=13, fontweight='bold')
ax.axhline(0, color='black', linewidth=0.8)
for b, v in zip(bars, perf['avg_pnl']):
    ax.text(b.get_x()+b.get_width()/2, v + (2 if v>=0 else -6), f'${v:.0f}', ha='center', fontsize=10)
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig('chart_avgpnl.png', dpi=150)
plt.close()

# 3. Trade volume (count) by sentiment
vol = df['classification'].value_counts().reindex(ORDER)
fig, ax = plt.subplots(figsize=(8,5))
bars = ax.bar(vol.index, vol.values, color=[COLORS[c] for c in vol.index])
ax.set_ylabel('Number of Trades')
ax.set_title('Trading Activity by Market Sentiment', fontsize=13, fontweight='bold')
for b, v in zip(bars, vol.values):
    ax.text(b.get_x()+b.get_width()/2, v+800, f'{v:,}', ha='center', fontsize=10)
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig('chart_volume.png', dpi=150)
plt.close()

# 4. Long vs Short bias when opening new positions, by sentiment
open_trades = df[df['Direction'].isin(['Open Long','Open Short'])]
mix = pd.crosstab(open_trades['classification'], open_trades['Direction'], normalize='index').reindex(ORDER) * 100
fig, ax = plt.subplots(figsize=(8,5))
ax.bar(mix.index, mix['Open Long'], label='Open Long', color='#2A9D8F')
ax.bar(mix.index, mix['Open Short'], bottom=mix['Open Long'], label='Open Short', color='#E76F51')
ax.set_ylabel('Share of New Positions (%)')
ax.set_title('Long vs. Short Positioning by Market Sentiment', fontsize=13, fontweight='bold')
ax.axhline(50, color='black', linewidth=0.8, linestyle='--', alpha=0.5)
ax.legend(loc='upper right')
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig('chart_longshort.png', dpi=150)
plt.close()

# 5. Daily PnL vs Fear/Greed index value over time (dual axis)
daily_sorted = daily.sort_values('date')
fig, ax1 = plt.subplots(figsize=(11,5.5))
ax2 = ax1.twinx()
ax1.plot(daily_sorted['date'], daily_sorted['daily_pnl'].rolling(7).mean(), color='#264653', linewidth=1.6, label='7-day avg daily PnL')
ax2.plot(daily_sorted['date'], daily_sorted['value'], color='#E9C46A', linewidth=1.2, alpha=0.8, label='Fear/Greed Index')
ax1.set_ylabel('7-day Avg Daily Closed PnL (USD)', color='#264653')
ax2.set_ylabel('Fear/Greed Index (0-100)', color='#B8860B')
ax1.set_title('Trader PnL Trend vs. Market Sentiment Over Time', fontsize=13, fontweight='bold')
ax1.axhline(0, color='gray', linewidth=0.6)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1+lines2, labels1+labels2, loc='upper left', fontsize=9)
plt.tight_layout()
plt.savefig('chart_timeseries.png', dpi=150)
plt.close()

# 6. Avg trade size by sentiment
size_by_sent = df.groupby('classification')['Size USD'].mean().reindex(ORDER)
fig, ax = plt.subplots(figsize=(8,5))
bars = ax.bar(size_by_sent.index, size_by_sent.values, color=[COLORS[c] for c in size_by_sent.index])
ax.set_ylabel('Average Trade Size (USD)')
ax.set_title('Average Position Size by Market Sentiment', fontsize=13, fontweight='bold')
for b, v in zip(bars, size_by_sent.values):
    ax.text(b.get_x()+b.get_width()/2, v+80, f'${v:,.0f}', ha='center', fontsize=10)
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig('chart_size.png', dpi=150)
plt.close()

print("Charts saved.")
