# backtest/ — The Excel Workbook

## Files

- **Crude_Oil_Backtest.xlsx**: The main working spreadsheet. Four sheets: Tracking, Data, Strategy, Results.

## How to Use

### 1. Tracking Sheet (Your Daily Habit)

**Purpose:** Record prices and fundamentals every day for 12 weeks.

**What you see:**
- Date (Mon–Sat, no weekends)
- WTI price (you update daily at 9 AM)
- Brent price (you update daily)
- WTI–Brent Spread (automatic formula)
- US crude inventory (EIA releases weekly)
- Refinery utilisation (EIA releases weekly)
- Event column (e.g., "OPEC meeting")
- Notes column (your analysis: "Why did the price move?")

**The first ~50 rows are pre-filled with real data from April–July 2026.**
The rest (through Sep 15) are blank and waiting for you to fill in as each day passes.

**Why this matters:** By tracking daily, you build market intuition. You'll notice correlations (e.g., when inventory falls, does price rise?). You'll see whether your notes predicted the next day's move. This is real trader's work.

### 2. Data Sheet (Full History + Derived Columns)

**Purpose:** 11.5 years of prices and computed indicators.

**What you see:**
- Date (2896 rows, Jan 2015 – Jul 2026)
- WTI_Close (daily closing price)
- Brent_Close (daily closing price)
- WTI_20MA (formula: 20-day moving average, *after row 21*)
- Deviation_% (formula: how far below/above the average, as a percentage)

**The formulas:**
```
WTI_20MA (row 22+):  =AVERAGE(B{row-19}:B{row})
Deviation_%:         =(B{row}-D{row})/D{row}*100
```

Every row with a negative deviation% is a potential BUY signal (if <−5%), and every row with positive deviation% is a SELL signal.

**Don't modify:** Dates and prices are raw. Only add new price rows if you download fresh data and extend the backtest.

### 3. Strategy Sheet (The Trading Logic, Day by Day)

**Purpose:** Execute the mean-reversion rule on every day of history. This is where the trades happen.

**What you see:**
- Date, Price (pulled from Data sheet)
- Signal (BUY / SELL / HOLD, computed by IF formulas)
- Entry_Price (the price at which you bought, or blank if not in position)
- Exit_Price (the price at which you sold, or blank if in position)
- Trade_P&L_% (profit or loss as a percentage, only filled on SELL days)
- Position (IN or OUT — tracks whether you're currently holding)
- Cumulative_P&L_% (running total of all trade returns — this is the equity curve)
- Running_Peak (the highest cumulative P&L reached so far)
- Drawdown (how far below the peak you currently are)

**Key formula (the rule itself) in the Signal column:**
```
=IF(Data!D{row}="","HOLD",
   IF(AND(G{row-1}<>"IN",Data!E{row}<-5),"BUY",
   IF(AND(G{row-1}="IN",Data!E{row}>0),"SELL","HOLD")))
```

Translation:
- If no MA yet (first 21 days): HOLD
- If not in position AND deviation < −5%: BUY
- If in position AND deviation > 0%: SELL
- Otherwise: HOLD

**Every row is auditable.** You can see the exact buy/sell dates and prices for all 59 completed trades.

### 4. Results Sheet (Summary Statistics & Equity Curve Chart)

**Purpose:** Aggregate all 59 trades into summary metrics.

**What you see:**
- **Performance Metrics table:**
  - Total Trades: 59
  - Winning Trades: 42
  - Losing Trades: 17
  - Win Rate: 71.2%
  - Average Win: +5.32%
  - Average Loss: −8.76%
  - Profit Factor: 1.50 (for every $1 lost, $1.50 won)
  - Total P&L: +74.5 pct-pts
  - Max Drawdown: −82.4 pct-pts
  - Buy & Hold: +35.5%
  - Outperformance: +39 pct-pts

All computed with formulas like:
```
Win Rate = COUNTIF(Strategy!F2:F{last},">0") / COUNTIF(Strategy!F2:F{last},"<>") * 100
Profit Factor = SUMIF(Strategy!F2:F{last},">0") / ABS(SUMIF(Strategy!F2:F{last},"<0"))
```

- **Equity curve chart:** A line plot showing cumulative P&L over time (2015–2026).

**Don't modify:** These are all formulas reading from the Strategy sheet. If you change the rule (e.g., threshold from −5% to −7%), everything recalculates automatically.

## How to Extend It

### Test a different threshold (e.g., −7% instead of −5%)

1. Go to Strategy sheet, Signal column
2. Change `Data!E{row}<-5` to `Data!E{row}<-7`
3. Watch all metrics recalculate instantly

### Add a stop-loss (e.g., −4% max loss per trade)

In the Strategy sheet, modify Entry_Price logic to track a stop-loss exit. This is a bit trickier in Excel; see docs/NEXT_STEPS.md for guidance.

### Test on Brent instead of WTI

1. Duplicate the Data sheet (call it "Data_Brent")
2. In that copy, change the price source to column C (Brent)
3. Duplicate Strategy sheet, point it to the Brent data
4. Compare results

### Add transaction costs

In the Trade_P&L_% column, subtract 0.10 from every trade:
```
=IF(E{row}="",(E{row}-D{row})/D{row}*100 - 0.10,"")
```

Watch the bottom line change (should drop from +74.5% to ~+70-72% depending on cost model).

## Quick Facts

- **2,896 rows** of price data
- **59 completed trades** (one BUY followed by one SELL)
- **71.2% win rate**, but largest loser (−39.8%) is larger than largest winner (+11.3%)
- **All formulas visible** — no macros, no black boxes
- **Fully auditable** — click any cell, see the formula

## Files Included With This

- The main workbook reads from CSV files (prices_full.csv, eia_inventory.csv, eia_refutil.csv) that are pre-loaded
- If you want to update prices, download fresh CSVs and paste them in the Data sheet
