# 📈 Simple Stock Options Analyzer

A simple Python program that analyzes stocks for covered call opportunities.

## 🚀 What it does:
- Asks you to input stock tickers
- Shows the stock's volatility (20-day)
- Displays covered call opportunities for the next two expiration dates
- Shows 10 strike prices above current price with premiums and annualized returns

## 📦 Installation:
```bash
pip install -r requirements.txt
```

## 🎯 Usage:
```bash
python simple_stock_analyzer.py
```

## 📊 Example Output:
```
📊 ANALYSIS FOR AAPL
============================================================

💰 Current Price: $211.27
📈 Volatility (20-day): 25.3%

🎯 COVERED CALL OPPORTUNITIES:
----------------------------------------

📅 Expiration 1: 2024-08-02 (5 days)
------------------------------
Strike     Premium    Annualized Return  
----------------------------------------
$215.00    $2.45      85.2%
$220.00    $1.23      42.1%
$225.00    $0.67      21.8%
...
```

## ⚠️ Disclaimer:
This is for educational purposes only. Not financial advice. 