# 🚀 Quick Start Guide

## Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Test installation:**
```bash
python test_installation.py
```

## Running the Application

### Web Interface (Recommended)
```bash
streamlit run app.py
```
Then open your browser to `http://localhost:8501`

### Command Line Demo
```bash
python run_demo.py
```

## Features

### 📊 Weekly Recommendations
- Analyzes 50+ stocks automatically
- Ranks by covered call score (0-68 points)
- Shows best options opportunities
- Exports to CSV

### 🔍 Individual Stock Analysis
- Enter any stock symbol (e.g., AAPL, MSFT)
- Comprehensive fundamental analysis
- Technical indicators (RSI, MACD, etc.)
- Options chain analysis

### 📈 What the App Does

**Fundamental Analysis:**
- Market cap, P/E ratio, ROE, debt/equity
- Current ratio, profit margins, growth rates
- Dividend yield and beta

**Technical Analysis:**
- RSI, moving averages, MACD
- Bollinger Bands, volatility
- Price action indicators

**Options Analysis:**
- Strike price recommendations
- Premium calculations
- Annualized return estimates
- Days to expiration

**Scoring System:**
- Fundamental factors (40 points max)
- Technical indicators (13 points max)
- Options opportunities (15 points max)
- **Total: 68 points maximum**

## Sample Results

From the demo, top recommendations include:
- **QCOM**: Score 66, 1120% annualized return
- **EOG**: Score 66, 622% annualized return  
- **AXP**: Score 66, 1033% annualized return

## Configuration

Edit `config.py` to customize:
- Scoring weights
- Stock lists
- Analysis parameters
- Risk thresholds

## Risk Warnings

⚠️ **Important Disclaimers:**
- This is for educational purposes only
- Not financial advice
- Options trading involves substantial risk
- Always do your own research
- Consult a financial advisor

## Support

If you encounter issues:
1. Check `test_installation.py` output
2. Verify internet connection
3. Ensure all dependencies installed
4. Check stock symbol validity

---

**Happy Trading! 📈💰** 