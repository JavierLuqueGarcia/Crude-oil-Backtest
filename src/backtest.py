#!/usr/bin/env python3
"""
backtest.py
Implements and runs the mean-reversion trading rule on WTI crude oil.

Rule:
  1. Compute 20-day moving average (MA20) and deviation: (price - MA20) / MA20 * 100
  2. If not in position AND deviation < -5%: BUY
  3. If in position AND deviation > 0%: SELL
  4. Otherwise: HOLD

Outputs:
  - trades.csv: all completed trades (entry, exit, P&L)
  - stats.json: headline metrics
  - Console output: summary results
"""

import pandas as pd
import json
import os

def run_backtest(prices_df, entry_threshold=-5.0, exit_threshold=0.0):
    """
    Run the mean-reversion backtest.
    
    Args:
        prices_df: DataFrame with Date index and 'WTI' column
        entry_threshold: deviation % below MA to trigger BUY (default -5%)
        exit_threshold: deviation % above which to SELL (default 0%)
    
    Returns:
        Dictionary with results
    """
    
    prices = prices_df['WTI'].copy()
    
    # Compute 20-day moving average and deviation
    ma20 = prices.rolling(20).mean()
    deviation = (prices - ma20) / ma20 * 100
    
    # Initialize tracking variables
    trades = []
    in_position = False
    entry_price = 0
    entry_date = None
    position_peak = 0
    
    equity = []
    equity_dates = []
    cumulative_pnl = 0
    
    # Walk through every day
    for i in range(len(prices)):
        date = prices.index[i]
        price = prices.iloc[i]
        dev = deviation.iloc[i]
        
        # Skip if no MA yet (first 20 days)
        if pd.isna(dev):
            continue
        
        # Check signals
        buy_signal = not in_position and dev < entry_threshold
        sell_signal = in_position and dev > exit_threshold
        
        # Execute trades
        if buy_signal:
            in_position = True
            entry_price = price
            entry_date = date
            position_peak = price
        
        elif sell_signal:
            exit_price = price
            pnl_pct = (exit_price - entry_price) / entry_price * 100
            
            # Record the trade
            trades.append({
                'entry_date': entry_date,
                'exit_date': date,
                'entry': round(entry_price, 2),
                'exit': round(exit_price, 2),
                'pnl': round(pnl_pct, 2)
            })
            
            # Update cumulative P&L
            cumulative_pnl += pnl_pct
            equity.append(cumulative_pnl)
            equity_dates.append(date)
            
            in_position = False
    
    # Compile results
    trades_df = pd.DataFrame(trades)
    
    if len(trades_df) > 0:
        pnl = trades_df['pnl']
        wins = (pnl > 0).sum()
        losses = (pnl < 0).sum()
        win_rate = (wins / len(pnl)) * 100 if len(pnl) > 0 else 0
        avg_win = pnl[pnl > 0].mean() if (pnl > 0).any() else 0
        avg_loss = pnl[pnl < 0].mean() if (pnl < 0).any() else 0
        profit_factor = pnl[pnl > 0].sum() / abs(pnl[pnl < 0].sum()) if (pnl < 0).any() else 0
        total_pnl = pnl.sum()
        best_trade = pnl.max()
        worst_trade = pnl.min()
        
        # Drawdown calculation
        if len(equity) > 0:
            cum_array = pd.Series(equity)
            peak = cum_array.cummax()
            drawdown = cum_array - peak
            max_drawdown = abs(drawdown.min())
        else:
            max_drawdown = 0
        
        # Buy & hold baseline
        bh_return = (prices.iloc[-1] - prices.iloc[0]) / prices.iloc[0] * 100
    else:
        win_rate = avg_win = avg_loss = profit_factor = total_pnl = best_trade = worst_trade = max_drawdown = bh_return = 0
        wins = losses = 0
    
    return {
        'trades': trades_df,
        'stats': {
            'n_trades': len(trades_df),
            'wins': wins,
            'losses': losses,
            'win_rate': round(win_rate, 1),
            'avg_win': round(avg_win, 2),
            'avg_loss': round(avg_loss, 2),
            'profit_factor': round(profit_factor, 2),
            'total_pnl': round(total_pnl, 1),
            'best_trade': round(best_trade, 1),
            'worst_trade': round(worst_trade, 1),
            'max_drawdown': round(max_drawdown, 1),
            'buy_hold_return': round(bh_return, 1),
            'outperformance': round(total_pnl - bh_return, 1),
        }
    }

if __name__ == "__main__":
    print("=" * 60)
    print("CRUDE OIL MEAN-REVERSION BACKTEST")
    print("=" * 60)
    
    # Load prices
    if not os.path.exists('data/prices_full.csv'):
        print("✗ Error: data/prices_full.csv not found. Run download_data.py first.")
        exit(1)
    
    prices_df = pd.read_csv('data/prices_full.csv', parse_dates=['Date'], index_col='Date')
    print(f"Loaded {len(prices_df)} days of price data ({prices_df.index[0].date()} to {prices_df.index[-1].date()})")
    
    # Run backtest with default parameters (-5% entry, 0% exit)
    print("\nRunning backtest...")
    print("  Entry: Buy when price falls >5% below 20-day average")
    print("  Exit:  Sell when price recovers above average")
    
    result = run_backtest(prices_df, entry_threshold=-5.0, exit_threshold=0.0)
    trades = result['trades']
    stats = result['stats']
    
    # Save trades
    os.makedirs('results', exist_ok=True)
    trades.to_csv('results/trade_log.csv', index=False)
    print(f"\n✓ Trades saved to results/trade_log.csv ({len(trades)} trades)")
    
    # Save stats
    with open('results/performance_metrics.json', 'w') as f:
        json.dump(stats, f, indent=2)
    print(f"✓ Metrics saved to results/performance_metrics.json")
    
    # Print summary
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"Total trades:      {stats['n_trades']}")
    print(f"Winning trades:    {stats['wins']} ({stats['win_rate']}% win rate)")
    print(f"Losing trades:     {stats['losses']}")
    print(f"Avg win:           +{stats['avg_win']}%")
    print(f"Avg loss:          {stats['avg_loss']}%")
    print(f"Profit factor:     {stats['profit_factor']}")
    print(f"\nTotal P&L:         +{stats['total_pnl']} pct-pts")
    print(f"Best trade:        +{stats['best_trade']}%")
    print(f"Worst trade:       {stats['worst_trade']}%")
    print(f"Max drawdown:      −{stats['max_drawdown']} pct-pts")
    print(f"\nBuy & hold:        +{stats['buy_hold_return']}%")
    print(f"Outperformance:    +{stats['outperformance']} pct-pts")
    print("=" * 60)
    
    # Sample trades
    if len(trades) > 0:
        print("\nFirst 3 trades:")
        print(trades.head(3).to_string(index=False))
