# Crude Oil Mean-Reversion Backtest

A complete, reproducible study of a simple trading rule applied to 11.5 years of real crude oil market data, with full documentation, code, and analysis for anyone to understand and audit.

**Key Results:**
- **59 trades** tested on 2,896 trading days (Jan 2015 – Jul 2026)
- **71.2% win rate** (42 winners, 17 losers)
- **+74.5 percentage points** total return
- **+39 percentage points** outperformance vs. buy-and-hold (+35.5%)
- **Honest limitations:** no stop-loss; ignores transaction costs, slippage, roll yield

---

## Quick Start: Where to Go

- **New to this project?** Read [reports/Crude_Oil_Backtest_Report.pdf](reports/Crude_Oil_Backtest_Report.pdf) A 20-page scientific report that explains every concept from scratch, with figures.
- **Want to see the data?** Check [data/](data/) for all CSVs (prices, inventory, trades).
- **Want to run it yourself?** See [src/README.md](src/README.md) and [backtest/README.md](backtest/README.md).
- **Don't understand a term?** See [docs/GLOSSARY.md](docs/GLOSSARY.md) (36 terms explained).

---

## What is this?

A **backtest** is replaying a trading rule on historical data to measure how it would have performed. This project:

1. **Defines a rule precisely**: Buy WTI crude when its price falls >5% below its 20-day average; sell when it recovers above the average.
2. **Tests it on real data**: 2,896 trading days of WTI and Brent prices (Yahoo Finance) + weekly US crude inventory and refinery utilization (EIA).
3. **Records every trade**: 59 completed round-trips, from entry to exit, with P&L.
4. **Reports honestly**: Shows what worked, what failed (the −39.8% COVID trade), and what wasn't modeled (costs, slippage).

The goal is to demonstrate:
- Can a mechanical rule (no human judgment) capture patterns in oil?
- What's the honest cost of ignoring real-world frictions?
- What would you need to do to deploy this in practice?

---

## The Files

| Path | What it contains |
|------|---|
| [`reports/`](reports/) | Full scientific report (PDF) with 9 figures, abstract, methodology, results, discussion, glossary |
| [`backtest/`](backtest/) | Excel workbook with live formulas: Tracking (12-week log), Data (full history + MA), Strategy (signals & trades), Results |
| [`data/`](data/) | Raw CSVs: prices, inventory, refinery utilisation, all 59 trades |
| [`src/`](src/) | Python scripts to fetch fresh data, run the backtest, compute metrics, generate figures |
| [`figures/`](figures/) | 9 publication-ready PNG charts |
| [`docs/`](docs/) | Methodology, glossary, limitations, next steps |
| [`results/`](results/) | Summary statistics and trade log (JSON, CSV, TXT) |

---

## The Strategy Rule (In 4 Steps)

```
1. Compute: WTI 20-day moving average, and deviation = (price - MA) / MA × 100
2. If no position is open AND deviation < -5% (price >5% below average):  BUY
3. If position is open AND deviation > 0% (price back above average):      SELL
4. Otherwise:  HOLD (do nothing)
```

No forecasting. No news reading. No judgement. Mechanical.

---

## Results Summary

| Metric | Value | Meaning |
|--------|-------|---------|
| **Total trades** | 59 | The rule triggered about 5 per year |
| **Win rate** | 71.2% | 7 out of 10 trades were profitable |
| **Best trade** | +11.3% | Single trade return |
| **Worst trade** | −39.8% | Entered Feb 2020, held through COVID crash (no stop-loss) |
| **Avg win** | +5.32% | Typical profitable trade |
| **Avg loss** | −8.76% | Typical losing trade (larger than avg win!) |
| **Total P&L** | +74.5 pct-pts | Sum of all 59 trades |
| **Buy & hold** | +35.5% | Benchmark: buy WTI in 2015, hold to 2026 |
| **Outperformance** | +39 pct-pts | Strategy roughly doubled the do-nothing baseline |
| **Max drawdown** | −82.4 pct-pts | Deepest point below previous peak (2020) |

---

## Critical Limitations (Read This Before Assuming Profit)

This backtest shows what *would have worked in historical data, **not** what will work in the future. Reasons to be cautious:

- **Transaction costs ignored**: Real trading costs ~$0.05–0.10/bbl per side. Over 59 trades, that's several percentage points of drag.
- **Slippage ignored**: Prices you actually fill at are usually worse than the closing price used in the backtest, especially in fast-falling markets (when this rule buys).
- **Roll costs ignored**: Holding futures continuously in contango silently loses money each month as you roll into the more expensive next contract.
- **No stop-loss**: The −39.8% COVID trade shows what happens when you ride a crash all the way down. A −4% stop-loss would have capped it, but cost other trades room to recover.
- **Parameter luck possible**: The −5% and 20-day numbers were not optimized; but published rules risk fitting the past (overfitting). Robustness checks (−3%, −7%, Brent) are proposed in [docs/NEXT_STEPS.md](docs/NEXT_STEPS.md).

**Bottom line:** This is a real pattern in real data. But the headline +74.5% is an upper bound on real profit, not a forecast.

---

## How to Reproduce

**In Excel (easiest):**
1. Open `backtest/Crude_Oil_Backtest.xlsx`
2. See the Tracking sheet (last 12 weeks, pre-filled)
3. See the Data sheet (full history, formulas for MA and deviation visible)
4. See the Strategy sheet (every day, every signal, every trade)
5. See the Results sheet (summary metrics and equity curve chart)

**In Python (to extend or modify):**
1. Install dependencies: `pip install -r src/requirements.txt`
2. Download fresh data: `python src/download_data.py`
3. Run the backtest: `python src/backtest.py`
4. Generate figures: `python src/analysis.py`
5. See `src/README.md` for details

---

## Key Concepts Explained

**WTI**: West Texas Intermediate, the US oil benchmark. **Brent**: The global benchmark. Both trade as futures (contracts for delivery on a future date). **Spot price**: The price for delivery today. **Contango**: A futures curve where future months cost more (signals ample supply). **Backwardation**: Future months cheaper (signals tight supply). **20-day moving average**: The average of the last 20 daily prices, a one-month smoothed view. **Mean reversion**: The tendency of a price that has swung far from its recent average to drift back. **P&L**: Profit and loss. **Equity curve**: The running total of all trade returns.

See [docs/GLOSSARY.md](docs/GLOSSARY.md) for 36 full definitions.

---


This project was built as part of a commodity-trading preparation programme to demonstrate:

1. **Quantitative thinking**: from hypothesis (mean reversion exists) to precise rule to empirical test.
2. **Data discipline**: real, auditable data; formulas visible; trade-by-trade record; honest caveats.
3. **Communication**: A 20-page report that explains every concept so someone new to markets can follow.
4. **Tool fluency**: Excel formulas for backtesting, Python for data pipelines, charting, metrics.
5. **Industry awareness**: Understanding of contango/backwardation, inventory signals, roll costs, real-world constraints.

**Not being claimed:** this rule is ready to trade live, or that past performance predicts the future. **What is being claimed:** here's a hypothesis about oil markets, here's how I tested it rigorously, here's what the data shows, and here's what I'd ignore if I wanted to claim profit.

---

## Next Steps / Extensions

See [docs/NEXT_STEPS.md](docs/NEXT_STEPS.md) for:
- Adding a −4% stop-loss and re-testing
- Testing −3% and −7% thresholds (robustness)
- Repeating on Brent instead of WTI
- Subtracting realistic costs
- Investigating the recent 12-week puzzle (prices down, inventory down — why?)

---

## Data Sources

- **Prices**: Yahoo Finance, tickers CL=F (WTI) and BZ=F (Brent), 2015-01-02 to 2026-07-10
- **Inventory & refinery data**: U.S. Energy Information Administration, Weekly Petroleum Status Report
- **Report figures**: Generated from real data using Python (matplotlib)

---

## License

[MIT License](LICENSE)  use, modify, and share freely.

---

## Questions?

- **How do I understand this?** Start with the [report PDF](reports/Crude_Oil_Backtest_Report.pdf).
- **How do I run it?** See [backtest/README.md](backtest/README.md) (Excel) or [src/README.md](src/README.md) (Python).
- **What do these terms mean?** See [docs/GLOSSARY.md](docs/GLOSSARY.md).
- **What are the weaknesses?** See [docs/LIMITATIONS.md](docs/LIMITATIONS.md).
- **What should I test next?** See [docs/NEXT_STEPS.md](docs/NEXT_STEPS.md).

---


