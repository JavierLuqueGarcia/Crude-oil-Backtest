# READ ME FIRST — GitHub Organization Guide

This document explains everything in `/mnt/user-data/outputs/` and how to organize it on GitHub.

---

## What You Have

###  Core Project Files

1. **Crude_Oil_Backtest.xlsx**: The complete Excel workbook
   - Tracking sheet: 12-week daily log (pre-filled through July 10, blank through Sep 15)
   - Data sheet: 2,896 days of prices with formulas
   - Strategy sheet: day-by-day signals and all 59 trades
   - Results sheet: summary metrics and equity curve chart
   - **Action:** Copy to `backtest/` folder on GitHub

2. **Crude_Oil_Backtest_Report.pdf**: 20-page scientific report
   - Complete narrative with 9 figures, abstract, methodology, results, discussion, glossary
   - Written so anyone without finance knowledge can understand
   - **Action:** Copy to `reports/` folder on GitHub

3. **Crude_Oil_Backtest_Report.docx**: Editable version of the report
   - Same content as PDF, but you can modify if needed
   - **Action:** Copy to `reports/` folder on GitHub

### Data Files (in `/mnt/user-data/outputs/`)

These CSVs are referenced in the Excel workbook and Python scripts:
- `prices_full.csv`: 2,896 rows of WTI and Brent daily closing prices (2015-2026)
- `eia_inventory.csv`: US crude inventories (weekly)
- `eia_refutil.csv`: US refinery utilization (weekly)
- `trades.csv`: All 59 completed trades with entry, exit, P&L
- **Action:** Copy to `data/` folder on GitHub

### 📈 Figures (9 PNG charts)

All generated from real data and ready for presentation:
- `fig1_wti_history.png`: 11.5 years of WTI price
- `fig2_wti_brent_spread.png`: Both benchmarks and their spread
- `fig3_meanreversion.png`: The concept on 2019 real data
- `fig4_curve.png`: Contango vs backwardation schematic
- `fig5_equity.png`: Your equity curve (cumulative P&L)
- `fig6_histogram.png`: All 59 trades ranked
- `fig7_vs_bh.png`: Strategy vs buy-and-hold
- `fig8_tracking.png`: Last 12 weeks (prices + inventory)
- `fig9_drawdown.png`: Underwater plot (drawdown over time)
- **Action:** Copy to `figures/` folder on GitHub

### 📄 Template Files (Markdown for README files)

Use these to populate each folder on GitHub with documentation:

1. **README_TEMPLATE.md** (rename to `README.md` in root)
   - Main entry point for your repo
   - Quick start guide, results summary, file navigation
   - Everything a recruiter sees first
   
2. **README_backtest.md** (copy to `backtest/README.md`)
   - Explains all four sheets in the Excel workbook
   - How to use, how to extend, quick facts
   
3. **README_data.md** (copy to `data/README.md`)
   - Defines each CSV file
   - Data sources and quality notes
   - How to refresh with new data
   
4. **README_src.md** (copy to `src/README.md`)
   - Quick start for Python code
   - What each script does (download_data, backtest, analysis)
   
5. **docs_LIMITATIONS.md** (rename to `docs/LIMITATIONS.md`)
   - Honest weaknesses: costs, slippage, roll yield, no stop-loss
   - What the backtest does/doesn't prove
   - Path to credibility

### 🔧 Setup and Structure Files

- **GITHUB_STRUCTURE.md**: Shows the exact folder layout
- **GITHUB_SETUP_CHECKLIST.md**: Step-by-step instructions to create the repo and populate it


---

## The GitHub Organization (Folder Structure)

```
crude-oil-backtest/
├── README.md                     ← Use README_TEMPLATE.md
├── .gitignore                    ← Use .gitignore_template
├── data/
│   ├── README.md                 ← Use README_data.md
│   ├── prices_full.csv
│   ├── eia_inventory.csv
│   ├── eia_refutil.csv
│   └── trades.csv
├── backtest/
│   ├── README.md                 ← Use README_backtest.md
│   └── Crude_Oil_Backtest.xlsx
├── figures/
│   ├── fig1_wti_history.png
│   ├── fig2_wti_brent_spread.png
│   ├── ... (all 9 figures)
│   └── README.md                 (optional: what each figure shows)
├── reports/
│   ├── Crude_Oil_Backtest_Report.pdf
│   └── Crude_Oil_Backtest_Report.docx
├── src/
│   ├── README.md                 ← Use README_src.md
│   ├── download_data.py
│   ├── backtest.py
│   ├── analysis.py
│   └── requirements.txt
├── results/
│   ├── summary_statistics.txt    (key metrics)
│   ├── trade_log.csv             (all 59 trades)
│   └── performance_metrics.json  (structured output)
└── docs/
    ├── METHODOLOGY.md            (explain the rule)
    ├── GLOSSARY.md               (36 terms)
    ├── LIMITATIONS.md            ← Use docs_LIMITATIONS.md
    └── NEXT_STEPS.md             (proposed robustness checks)
```

---

