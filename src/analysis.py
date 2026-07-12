#!/usr/bin/env python3
"""
analysis.py
Generates publication-ready figures from backtest data.

Creates 9 PNG files in figures/ folder:
  1. fig1_wti_history.png - 11.5 years of WTI prices
  2. fig2_wti_brent_spread.png - Both benchmarks + spread
  3. fig3_meanreversion.png - Concept on 2019 data
  4. fig4_curve.png - Contango vs backwardation schematic
  5. fig5_equity.png - Equity curve (cumulative P&L)
  6. fig6_histogram.png - Every trade ranked
  7. fig7_vs_bh.png - Strategy vs buy-and-hold
  8. fig8_tracking.png - Last 12 weeks (prices + inventory)
  9. fig9_drawdown.png - Underwater plot (drawdown)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Set style
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3

NAVY = '#1F4E5F'
ORANGE = '#E67E22'
GREEN = '#27AE60'
RED = '#C0392B'
BLUE = '#2E5C8A'

def load_data():
    """Load prices and trades."""
    prices = pd.read_csv('data/prices_full.csv', parse_dates=['Date'])
    trades = pd.read_csv('results/trade_log.csv', parse_dates=['entry_date', 'exit_date'])
    inv = pd.read_csv('data/eia_inventory.csv', parse_dates=['Date'])
    return prices, trades, inv

def fig1_wti_history(prices):
    """Figure 1: 11.5 years of WTI price history."""
    fig, ax = plt.subplots(figsize=(9, 4.2))
    ax.plot(prices['Date'], prices['WTI'], color=NAVY, lw=0.8)
    ax.set_title('Figure 1. WTI Crude Oil Front-Month Price, 2015–2026', fontweight='bold', fontsize=11)
    ax.set_ylabel('Price (US$ per barrel)')
    ax.set_xlabel('Year')
    ax.axhline(0, color='gray', lw=0.5)
    ax.annotate('April 2020:\nCOVID demand collapse\n(price briefly negative)',
                xy=(pd.Timestamp('2020-04-20'), 11), xytext=(pd.Timestamp('2021-02-01'), -8),
                fontsize=7.5, arrowprops=dict(arrowstyle='->', color=RED), color=RED)
    plt.tight_layout()
    plt.savefig('figures/fig1_wti_history.png', dpi=150)
    plt.close()
    print("✓ Figure 1: WTI history")

def fig2_wti_brent_spread(prices):
    """Figure 2: WTI vs Brent + spread."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 5.2), sharex=True, gridspec_kw={'height_ratios':[3,1]})
    ax1.plot(prices['Date'], prices['WTI'], color=NAVY, lw=0.7, label='WTI (US benchmark)')
    ax1.plot(prices['Date'], prices['Brent'], color=ORANGE, lw=0.7, label='Brent (global benchmark)')
    ax1.set_ylabel('Price (US$/bbl)')
    ax1.legend(loc='upper right', fontsize=8)
    ax1.set_title('Figure 2. WTI vs Brent, and the Spread Between Them', fontweight='bold', fontsize=11)
    spread = prices['Brent'] - prices['WTI']
    ax2.fill_between(prices['Date'], spread, color=GREEN, alpha=0.5)
    ax2.set_ylabel('Brent–WTI ($)')
    ax2.set_xlabel('Year')
    ax2.axhline(0, color='gray', lw=0.5)
    plt.tight_layout()
    plt.savefig('figures/fig2_wti_brent_spread.png', dpi=150)
    plt.close()
    print("✓ Figure 2: WTI vs Brent")

def fig3_meanreversion(prices):
    """Figure 3: Mean reversion concept on 2019 data."""
    prices['MA20'] = prices['WTI'].rolling(20).mean()
    prices['Dev'] = (prices['WTI'] - prices['MA20']) / prices['MA20'] * 100
    
    sub = prices[(prices['Date'] >= '2019-01-01') & (prices['Date'] <= '2019-12-31')].reset_index(drop=True)
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(sub['Date'], sub['WTI'], color=NAVY, lw=1.2, label='WTI daily price')
    ax.plot(sub['Date'], sub['MA20'], color=ORANGE, lw=1.5, label='20-day moving average', ls='--')
    ax.fill_between(sub['Date'], sub['MA20']*0.95, sub['MA20'], color=RED, alpha=0.12, label='Zone within 5% below average')
    buys = sub[sub['Dev'] < -5]
    ax.scatter(buys['Date'], buys['WTI'], color=GREEN, s=45, zorder=5, marker='^', label='BUY trigger (>5% below avg)')
    ax.set_title('Figure 3. The Mean-Reversion Idea, Illustrated (WTI, 2019)', fontweight='bold', fontsize=11)
    ax.set_ylabel('Price (US$/bbl)')
    ax.set_xlabel('2019')
    ax.legend(loc='upper left', fontsize=8)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig('figures/fig3_meanreversion.png', dpi=150)
    plt.close()
    print("✓ Figure 3: Mean reversion concept")

def fig4_curve():
    """Figure 4: Contango vs backwardation schematic."""
    fig, (axa, axb) = plt.subplots(1, 2, figsize=(9, 3.8))
    months = np.arange(1, 13)
    contango = 70 + months*0.8
    backwardation = 78 - months*0.7
    axa.plot(months, contango, 'o-', color=BLUE, lw=2)
    axa.set_title('Contango\n(future > today: ample supply)', fontsize=10, fontweight='bold')
    axa.set_xlabel('Months into the future')
    axa.set_ylabel('Futures price ($/bbl)')
    axa.grid(alpha=0.3)
    axb.plot(months, backwardation, 'o-', color=RED, lw=2)
    axb.set_title('Backwardation\n(future < today: supply is tight)', fontsize=10, fontweight='bold')
    axb.set_xlabel('Months into the future')
    axb.set_ylabel('Futures price ($/bbl)')
    axb.grid(alpha=0.3)
    fig.suptitle('Figure 4. The Two Shapes of the Futures Curve', fontweight='bold', fontsize=11, y=1.02)
    plt.tight_layout()
    plt.savefig('figures/fig4_curve.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("✓ Figure 4: Contango/backwardation")

def fig5_equity(trades):
    """Figure 5: Equity curve."""
    if len(trades) == 0:
        return
    pnl = trades['pnl'].values
    cum = np.cumsum(pnl)
    fig, ax = plt.subplots(figsize=(9, 4.2))
    ax.plot(range(len(cum)), cum, color=NAVY, lw=1.5)
    ax.fill_between(range(len(cum)), cum, color=NAVY, alpha=0.1)
    ax.set_title('Figure 5. Strategy Equity Curve — Cumulative Profit Over Time', fontweight='bold', fontsize=11)
    ax.set_ylabel('Cumulative P&L (%)')
    ax.set_xlabel('Trade number')
    ax.axhline(0, color='gray', lw=0.5)
    worst_idx = np.argmin(pnl)
    ax.annotate(f'Worst trade: {pnl[worst_idx]:.0f}%\n(no stop-loss)',
                xy=(worst_idx, cum[worst_idx]), xytext=(worst_idx+10, cum[worst_idx]+20),
                fontsize=8, color=RED, arrowprops=dict(arrowstyle='->', color=RED))
    plt.tight_layout()
    plt.savefig('figures/fig5_equity.png', dpi=150)
    plt.close()
    print("✓ Figure 5: Equity curve")

def fig6_histogram(trades):
    """Figure 6: Every trade ranked."""
    if len(trades) == 0:
        return
    pnl_sorted = trades['pnl'].sort_values(ascending=False).values
    colors = [GREEN if x > 0 else RED for x in pnl_sorted]
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.bar(range(len(pnl_sorted)), pnl_sorted, color=colors)
    ax.set_title('Figure 6. Every Trade Ranked by Profit/Loss', fontweight='bold', fontsize=11)
    ax.set_ylabel('Trade return (%)')
    ax.set_xlabel('Trade (sorted best → worst)')
    ax.axhline(0, color='black', lw=0.8)
    wins = (trades['pnl'] > 0).sum()
    losses = (trades['pnl'] < 0).sum()
    ax.text(0.02, 0.95, f'{wins} winners', transform=ax.transAxes, color=GREEN, fontweight='bold', va='top')
    ax.text(0.02, 0.88, f'{losses} losers', transform=ax.transAxes, color=RED, fontweight='bold', va='top')
    plt.tight_layout()
    plt.savefig('figures/fig6_histogram.png', dpi=150)
    plt.close()
    print("✓ Figure 6: Trade histogram")

def fig7_vs_bh(prices, trades):
    """Figure 7: Strategy vs buy-and-hold."""
    if len(trades) == 0:
        return
    bh = (prices['WTI'] / prices['WTI'].iloc[0] - 1) * 100
    cum_pnl = np.cumsum(trades['pnl'].values)
    fig, ax = plt.subplots(figsize=(9, 4.2))
    ax.plot(prices['Date'], bh, color=ORANGE, lw=1.3, label='Buy & Hold (own WTI the whole time)')
    # Map trades to dates for plotting
    trade_dates = trades['exit_date'].values
    ax.plot(trade_dates, cum_pnl, color=NAVY, lw=1.5, label='Mean-Reversion Strategy')
    ax.set_title('Figure 7. Strategy vs. Simply Buying and Holding', fontweight='bold', fontsize=11)
    ax.set_ylabel('Cumulative return (%)')
    ax.set_xlabel('Year')
    ax.axhline(0, color='gray', lw=0.5)
    ax.legend(loc='upper left', fontsize=8.5)
    plt.tight_layout()
    plt.savefig('figures/fig7_vs_bh.png', dpi=150)
    plt.close()
    print("✓ Figure 7: Strategy vs buy-and-hold")

def fig8_tracking(prices, inv):
    """Figure 8: Last 12 weeks with prices and inventory."""
    cutoff = prices['Date'].max() - pd.Timedelta(weeks=12)
    recent = prices[prices['Date'] >= cutoff]
    inv_recent = inv[inv['Date'] >= cutoff]
    
    fig, ax1 = plt.subplots(figsize=(9, 4.4))
    ax1.plot(recent['Date'], recent['WTI'], color=NAVY, lw=1.3, label='WTI price')
    ax1.plot(recent['Date'], recent['Brent'], color=ORANGE, lw=1.3, label='Brent price')
    ax1.set_ylabel('Price (US$/bbl)', color=NAVY)
    ax1.set_xlabel('2026')
    ax2 = ax1.twinx()
    ax2.plot(inv_recent['Date'], inv_recent['Inventory_kbbl']/1000, color=GREEN, lw=2, marker='o', ms=4, label='US crude inventory')
    ax2.set_ylabel('US crude inventory (million bbl)', color=GREEN)
    ax1.set_title('Figure 8. The Last 12 Weeks: Prices Falling as Inventories Drew Down', fontweight='bold', fontsize=10.5)
    l1, lab1 = ax1.get_legend_handles_labels()
    l2, lab2 = ax2.get_legend_handles_labels()
    ax1.legend(l1+l2, lab1+lab2, loc='upper right', fontsize=8)
    ax1.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig('figures/fig8_tracking.png', dpi=150)
    plt.close()
    print("✓ Figure 8: Last 12 weeks tracking")

def fig9_drawdown(trades):
    """Figure 9: Underwater plot (drawdown)."""
    if len(trades) == 0:
        return
    pnl = trades['pnl'].values
    cum = np.cumsum(pnl)
    peak = np.maximum.accumulate(cum)
    dd = cum - peak
    fig, ax = plt.subplots(figsize=(9, 3.6))
    ax.fill_between(range(len(dd)), dd, color=RED, alpha=0.5)
    ax.set_title('Figure 9. "Underwater" Plot — How Far Below the Previous Peak', fontweight='bold', fontsize=11)
    ax.set_ylabel('Drawdown (pct-pts)')
    ax.set_xlabel('Trade number')
    ax.axhline(0, color='black', lw=0.6)
    plt.tight_layout()
    plt.savefig('figures/fig9_drawdown.png', dpi=150)
    plt.close()
    print("✓ Figure 9: Drawdown underwater plot")

if __name__ == "__main__":
    print("=" * 60)
    print("GENERATING ANALYSIS FIGURES")
    print("=" * 60)
    
    # Create figures folder
    os.makedirs('figures', exist_ok=True)
    
    # Load data
    prices, trades, inv = load_data()
    print(f"Loaded {len(prices)} price rows and {len(trades)} trades\n")
    
    # Generate all figures
    fig1_wti_history(prices)
    fig2_wti_brent_spread(prices)
    fig3_meanreversion(prices)
    fig4_curve()
    fig5_equity(trades)
    fig6_histogram(trades)
    fig7_vs_bh(prices, trades)
    fig8_tracking(prices, inv)
    fig9_drawdown(trades)
    
    print("\n" + "=" * 60)
    print("All figures saved to figures/ folder")
    print("=" * 60)
