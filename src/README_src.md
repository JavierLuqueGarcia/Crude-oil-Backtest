# src/ — Python Code

## Files

- **download_data.py** — Fetches fresh WTI/Brent prices from Yahoo Finance and EIA inventory/refinery data
- **backtest.py** — Implements the mean-reversion rule, runs it day by day, generates trades.csv
- **analysis.py** — Computes metrics, generates the 9 PNG figures
- **requirements.txt** — Dependencies (pandas, yfinance, matplotlib)

## Quick Start

```bash
pip install -r requirements.txt
python download_data.py        # Fetch latest data
python backtest.py              # Run the strategy
python analysis.py              # Generate figures
```

## What Each Script Does

### download_data.py
- Fetches CL=F and BZ=F from Yahoo Finance (2015–today)
- Fetches WCESTUS1 (inventory) and WPULEUS3 (refinery util) from EIA
- Saves to CSV files in data/
- Idempotent: safe to run weekly to keep data current

### backtest.py
- Reads prices_full.csv
- Implements the rule: buy when deviation < −5%, sell when deviation > 0%
- Outputs:
  - trades.csv (all 59 trades)
  - stats.json (headline metrics)
  - Console printout of key results

### analysis.py
- Reads prices and trades
- Generates 9 figures (PNG):
  - fig1_wti_history.png
  - fig2_wti_brent_spread.png
  - fig3_meanreversion.png (concept on 2019 data)
  - fig4_curve.png (contango/backwardation schematic)
  - fig5_equity.png (equity curve)
  - fig6_histogram.png (every trade ranked)
  - fig7_vs_bh.png (strategy vs buy-and-hold)
  - fig8_tracking.png (last 12 weeks)
  - fig9_drawdown.png (underwater plot)
- Saves all to figures/

## Notes

- All scripts are commented and readable
- No machine learning, no overfitting: the −5% and 20-day parameters are set, not optimized
- Scripts can be modified to test different thresholds (−3%, −7%), add stop-losses, etc.
- Output is deterministic: same input data → same results
