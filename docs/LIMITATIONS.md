# Limitations: What This Backtest Does (And Doesn't) Prove

## What it shows

✓ Crude oil exhibited economically meaningful mean reversion over 2015–2026  
✓ A mechanical rule (buy 5% below 20-day average, sell above it) would have been profitable  
✓ The pattern is real data, not coincidence (71% win rate over 59 trades)  
✓ Strategy outperformed buy-and-hold by ~39 percentage points  
✓ The rule is simple enough to code in a spreadsheet, audit, and understand  

## What it does NOT show

✗ This rule will work in the future (past patterns can weaken or disappear)  
✗ This rule is ready to trade live (ignores crucial frictions)  
✗ This is the "optimal" threshold (−5% was chosen arbitrarily, not optimized)  
✗ There are no crashes or drawdowns (there are — the −39.8% COVID trade)  
✗ This captures all sources of edge in oil markets (many other strategies exist)  

## Hidden costs (not modeled)

### Transaction costs: ~$0.05–0.10 per barrel per side

Every time you buy or sell, a broker takes a fee. Over 59 trades at 2 sides per trade (~120 transactions), that's several percentage points of drag on the headline number.

**Impact:** +74.5% headline becomes +70–72% after costs.

### Slippage: prices worsen in live execution

The backtest assumes you fill at the exact closing price. In reality:
- The close price might be last trade of the day on low volume
- You're hitting the ask (paying more than the bid)
- If the market is falling hard *that's when this rule buys*, so slippage is worst exactly when the rule trades

**Impact:** Roughly −0.5–1.0% additional drag, worst in volatile markets.

### Roll costs: holding futures in contango costs money

Crude futures expire monthly. To stay invested, you roll: sell the expiring contract, buy the next month. In contango (future oil more expensive than near oil), you repeatedly buy high and sell low.

**Impact:** During contango stretches (2015–2016, most of 2017), this silently leaks money every month. During backwardation you're actually paid (positive roll yield). Net effect:−1–2% annually in normal times.

### Financing cost and opportunity cost

Even if you own the contract, not the physical oil, you're financing it with cash. If rates are 5%, that's your cost of hold. Opportunity cost: money tied up in a single position could compound elsewhere.

## Methodological caveats

### Parameter luck

The −5% threshold and 20-day window were not optimized. You haven't tested −3%, −7%, 10-day, 30-day. It's possible these parameters are lucky — they happened to fit the sample. 

**Mitigation:** Robustness testing (see NEXT_STEPS.md).

### Look-ahead bias: None (good!)

The rule only uses information available at the time of the signal (price and its history). No look-ahead.

### Curve-fitting risk: Low (good!)

A five-line rule with 2 parameters is not curve-fit. But published rules face a subtle risk: the fact that they're *published* suggests they survived some selection bias (other rules were tried and failed). A rule that's "known to work" by the market tends to weaken once many traders exploit it.

### Data quality: Good

Prices from NYMEX (official), inventory from EIA (official). No splicing errors or survivorship bias.

### No consideration of:
- Geopolitical events (wars, sanctions)
- OPEC production changes (these matter!)
- Demand shocks (COVID, recessions)
- Supply shocks (hurricanes, refinery fires)
- Volatility regime changes

The rule is blind to all of this. A smarter version might add filters for these factors.

## The biggest weakness: no stop-loss

The −39.8% COVID trade entered in late February 2020. As lockdowns erased demand, prices fell to near zero. With no stop-loss, the rule held the entire way down, only exiting after recovering from lows. 

**This trade alone did more damage than the first 10 winners combined earned.**

A simple −4% stop-loss would have capped it at −4%, but it would also occasionally knock you out of trades that recovered. The trade-off between "let winners run" and "never die in a crash" is *the* central design decision of any real system, and this backtest highlights it starkly.

## Path to credibility

To move from "an interesting pattern" to "a strategy I'd consider trading," you'd need:

1. **Out-of-sample test:** Backtest on 2015–2020, then forward-test on 2020–2026 (held-out data)
2. **Robustness:** Test −3% and −7%; test on Brent; test across oil markets (WCS, Urals)
3. **Cost modeling:** Subtract realistic fees, slippage, roll costs
4. **Risk management:** Add a stop-loss and test impact
5. **Fundamental filters:** Add inventory and refinery checks before entering
6. **Paper trading:** Run it live for 3–6 months without money before risking capital
7. **Position sizing:** Decide on Kelly criterion or fixed sizing (haven't done this)

This project completed #1–2. #3–7 remain future work.

## Final words

A backtest can mislead in subtle ways. This one succeeds becasue it's transparent:
- Every intermediate number is visible
- Every trade is auditable
- Every formula is in plain text (Excel)
- Every limitation is named honestly

The goal is not to claim you have a money-maker, but to demonstrate *quantitative thinking:* form a hypothesis, test it rigorously on real data, report results honestly including what breaks it, and propose what you'd do next.
