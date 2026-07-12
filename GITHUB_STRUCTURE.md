# GitHub Repository Structure for Crude Oil Backtest Project

Your repo should look like this:

```
crude-oil-backtest/
├── README.md                          (ENTRY POINT — start here)
├── .gitignore
├── LICENSE (optional but professional)
│
├── data/
│   ├── README.md                      (explain data sources)
│   ├── prices_full.csv                (WTI & Brent 2015-2026, from Yahoo Finance)
│   ├── eia_inventory.csv              (US crude inventory, from EIA)
│   ├── eia_refutil.csv                (refinery utilization, from EIA)
│   └── trades.csv                     (all 59 trades: entry, exit, P&L)
│
├── src/
│   ├── README.md                      (code overview)
│   ├── download_data.py               (script to fetch fresh prices & EIA data)
│   ├── backtest.py                    (the mean-reversion rule, trade-by-trade)
│   ├── analysis.py                    (compute metrics, generate figures)
│   └── requirements.txt               (pandas, yfinance, matplotlib versions)
│
├── backtest/
│   ├── Crude_Oil_Backtest.xlsx        (the working spreadsheet — formulas visible)
│   └── README.md                      (explain each sheet: Tracking, Data, Strategy, Results)
│
├── figures/
│   ├── fig1_wti_history.png           (11.5-year price chart)
│   ├── fig2_wti_brent_spread.png      (both benchmarks + spread)
│   ├── fig3_meanreversion.png         (concept on 2019 real data)
│   ├── fig4_curve.png                 (contango vs backwardation schematic)
│   ├── fig5_equity.png                (the equity curve)
│   ├── fig6_histogram.png             (every trade ranked)
│   ├── fig7_vs_bh.png                 (strategy vs buy-and-hold)
│   ├── fig8_tracking.png              (last 12 weeks, prices vs inventory)
│   ├── fig9_drawdown.png              (underwater plot)
│   └── README.md                      (what each figure shows)
│
├── reports/
│   ├── Crude_Oil_Backtest_Report.pdf  (full 20-page scientific report)
│   └── Crude_Oil_Backtest_Report.docx (editable version)
│
├── results/
│   ├── summary_statistics.txt         (headline numbers: 71.2% win rate, +74.5% total, etc.)
│   ├── trade_log.csv                  (all 59 trades with dates, prices, P&L)
│   └── performance_metrics.json       (structured output for programmatic use)
│
└── docs/
    ├── METHODOLOGY.md                 (the strategy rule explained plainly)
    ├── GLOSSARY.md                    (all 36 terms from the report)
    ├── LIMITATIONS.md                 (honest weaknesses: costs, slippage, no stop-loss)
    └── NEXT_STEPS.md                  (proposed robustness checks & extensions)
```

## Key files to create or move:

1. **README.md** (top level) — your "landing page"
2. **.gitignore** — exclude temp files, not data or figures
3. Individual README.md files in data/, src/, backtest/, figures/, docs/
4. Move the Excel file into backtest/
5. Move figures into figures/
6. Move report into reports/
7. Export key numbers to results/summary_statistics.txt

