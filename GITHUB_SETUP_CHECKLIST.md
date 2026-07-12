# GitHub Setup Checklist

## Step 1: Create the repo

1. Go to GitHub.com and log in
2. Click "New repository"
3. Name it: **crude-oil-backtest**
4. Description: "A mean-reversion backtest on 11.5 years of WTI crude oil futures, with full scientific report, Excel model, and Python code."
5. Public (so recruiters can see)
6. Initialize with a README (you'll replace it)
7. Add .gitignore for Python
8. License: MIT (nice to have, not required)
9. Click "Create"

## Step 2: Clone to your machine

```bash
git clone https://github.com/YOUR_USERNAME/crude-oil-backtest.git
cd crude-oil-backtest
```

## Step 3: Create folder structure

```bash
mkdir -p data src backtest figures reports results docs
```

## Step 4: Create README and .gitignore files

Copy the template files provided:
- README.md (from README_TEMPLATE.md in this guide)
- .gitignore (from .gitignore_template)

Into the root of your repo:
```bash
cp /path/to/README_TEMPLATE.md README.md
cp /path/to/.gitignore_template .gitignore
```

## Step 5: Populate each folder

### data/
Move these files:
- prices_full.csv
- eia_inventory.csv
- eia_refutil.csv
- trades.csv

Create README.md in data/ (from README_data.md template)

### backtest/
Move:
- Crude_Oil_Backtest.xlsx

Create README.md in backtest/ (from README_backtest.md template)

### figures/
Move all 9 PNG files:
- fig1_wti_history.png through fig9_drawdown.png

Create README.md in figures/ explaining what each shows

### reports/
Move:
- Crude_Oil_Backtest_Report.pdf
- Crude_Oil_Backtest_Report.docx

### src/
Create these Python files (copy from your build scripts):
- download_data.py
- backtest.py
- analysis.py
- requirements.txt

Create README.md in src/ (from README_src.md template)

### results/
Create:
- summary_statistics.txt (key numbers)
- trade_log.csv (export from trades.csv)
- performance_metrics.json (export key stats as JSON)

### docs/
Create four markdown files:
- METHODOLOGY.md (explain the rule)
- GLOSSARY.md (36 terms from the report)
- LIMITATIONS.md (the honest weaknesses)
- NEXT_STEPS.md (proposed robustness checks)

Copy LIMITATIONS.md from the template provided.

## Step 6: Git add, commit, push

```bash
git add .
git commit -m "Initial commit: crude oil backtest with full documentation, data, and analysis"
git push origin main
```

## Step 7: Add GitHub metadata

1. Go to your repo on GitHub.com
2. Settings → About
3. Description: "A mean-reversion backtest on 11.5 years of crude oil futures"
4. Website: (leave blank or link to your portfolio)
5. Topics: add `trading`, `backtest`, `quantitative-analysis`, `commodities`, `python`
6. Click Save

## Step 8: Make it shine with a GitHub Pages (optional but nice)

If you want a landing page:
1. Settings → Pages
2. Choose "Deploy from branch" → main → /docs folder
3. Create index.html in docs/ with links to the report and repo

## Step 9: Verify

Visit https://github.com/YOUR_USERNAME/crude-oil-backtest

You should see:
- Clear folder structure
- Professional README with table of contents
- Link to the 20-page report (PDF)
- Link to the Excel workbook
- Data CSVs visible
- 9 figures
- Python code
- All with helpful READMEs in each folder

## What Recruiters Will See

They land on your repo and immediately see:
1. A clear title and purpose (the main README)
2. Key results: 71.2% win rate, +74.5% return, +39 vs buy-and-hold
3. The scientific report (click the PDF)
4. The Excel workbook (download to see formulas)
5. Data and code (fully reproducible)
6. Honest limitations (you know the weaknesses)
7. Proposed next steps (you're thinking ahead)

Result: "This person is serious about commodities, knows how to test ideas, and can communicate."

## Maintaining It

- Run `python src/download_data.py` weekly to keep prices fresh
- Re-run `python src/backtest.py` to update results (you'll extend through Sep 15)
- Commit changes: `git add . && git commit -m "Updated with data through [date]"`
- Push: `git push origin main`

By early September, when you apply, your repo will show the full 12-week tracking and the backtest extended through the application window.

## Pro Tips

- **Pin the README:** GitHub shows the main README first — make sure it's welcoming
- **Use badges:** Add badges for Python, Jupyter, License at the top of the README (optional)
- **Link to blog:** If you write market commentary, link it in the README
- **Keep it live:** The Tracking sheet updates every day through Sep 15 — that's powerful. "Most recently updated: [date]" at the bottom of README shows you're on it
- **Make it private for interviews:** Before interviews, you can temporarily make it private (Settings → Private) if they ask, then share the link. Most recruiters prefer seeing public work
