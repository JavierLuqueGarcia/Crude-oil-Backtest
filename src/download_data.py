#!/usr/bin/env python3
"""
download_data.py
Fetches fresh crude oil price data and EIA supply statistics.

Downloads:
  - WTI (CL=F) and Brent (BZ=F) front-month futures from Yahoo Finance
  - US crude inventory (WCESTUS1) from EIA
  - US refinery utilisation (WPULEUS3) from EIA

Saves to CSV files in data/ folder.
Safe to run weekly — overwrites old data with fresh data.
"""

import pandas as pd
import yfinance as yf
import urllib.request
from io import BytesIO
import os

def download_prices():
    """Download WTI and Brent futures prices from Yahoo Finance."""
    print("Downloading prices from Yahoo Finance...")
    try:
        wti = yf.download('CL=F', start='2015-01-01', progress=False)['Close']
        brent = yf.download('BZ=F', start='2015-01-01', progress=False)['Close']
        
        df = pd.concat([wti, brent], axis=1)
        df.columns = ['WTI', 'Brent']
        df = df.dropna(subset=['WTI'])
        df.index.name = 'Date'
        
        # Save to data/ folder
        os.makedirs('data', exist_ok=True)
        df.to_csv('data/prices_full.csv')
        print(f"✓ Prices saved: {len(df)} rows from {df.index[0].date()} to {df.index[-1].date()}")
        return df
    except Exception as e:
        print(f"✗ Error downloading prices: {e}")
        return None

def download_eia_inventory():
    """Download US crude inventory from EIA."""
    print("Downloading US crude inventory from EIA...")
    try:
        url = "https://www.eia.gov/dnav/pet/hist_xls/WCESTUS1w.xls"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        
        # Parse the Excel file
        df = pd.read_excel(BytesIO(data), sheet_name='Data 1', skiprows=2)
        df.columns = ['Date', 'Inventory_kbbl']
        df['Date'] = pd.to_datetime(df['Date'])
        
        os.makedirs('data', exist_ok=True)
        df.to_csv('data/eia_inventory.csv', index=False)
        print(f"✓ Inventory saved: {len(df)} weeks, latest = {df['Date'].max().date()}")
        return df
    except Exception as e:
        print(f"✗ Error downloading inventory: {e}")
        return None

def download_eia_refinery_util():
    """Download US refinery utilisation from EIA."""
    print("Downloading US refinery utilisation from EIA...")
    try:
        url = "https://www.eia.gov/dnav/pet/hist_xls/WPULEUS3w.xls"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        
        df = pd.read_excel(BytesIO(data), sheet_name='Data 1', skiprows=2)
        df.columns = ['Date', 'RefUtil_pct']
        df['Date'] = pd.to_datetime(df['Date'])
        
        os.makedirs('data', exist_ok=True)
        df.to_csv('data/eia_refutil.csv', index=False)
        print(f"✓ Refinery util saved: {len(df)} weeks, latest = {df['Date'].max().date()}")
        return df
    except Exception as e:
        print(f"✗ Error downloading refinery data: {e}")
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("CRUDE OIL DATA DOWNLOAD")
    print("=" * 60)
    download_prices()
    download_eia_inventory()
    download_eia_refinery_util()
    print("=" * 60)
    print("Done. Check data/ folder for CSV files.")
