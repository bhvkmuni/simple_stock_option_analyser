import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

def get_stock_data(symbol):
    """Get stock data and calculate volatility"""
    try:
        # Get stock data
        stock = yf.Ticker(symbol)
        data = stock.history(period="1y")
        
        if data.empty:
            return None, "No data found for this symbol"
        
        # Calculate volatility (20-day rolling standard deviation)
        data['Returns'] = data['Close'].pct_change()
        volatility = data['Returns'].rolling(window=20).std() * np.sqrt(252) * 100  # Annualized %
        current_volatility = volatility.iloc[-1]
        
        # Get current price
        current_price = data['Close'].iloc[-1]
        
        return {
            'symbol': symbol,
            'current_price': current_price,
            'volatility': current_volatility,
            'data': data
        }, None
        
    except Exception as e:
        return None, f"Error: {e}"

def calculate_probability_itm(current_price, strike, volatility, days_to_expiry, is_call):
    """Calculate probability of being in the money"""
    try:
        # Simple probability calculation using normal distribution
        # This is a rough approximation
        if days_to_expiry <= 0:
            return 0.0
        
        # Convert volatility to decimal
        vol_decimal = volatility / 100
        
        # Calculate d1 for Black-Scholes approximation
        time_to_expiry = days_to_expiry / 365
        if time_to_expiry <= 0:
            return 0.0
            
        d1 = (np.log(current_price / strike) + (0.05 + 0.5 * vol_decimal**2) * time_to_expiry) / (vol_decimal * np.sqrt(time_to_expiry))
        
        # Probability of being ITM (using normal CDF approximation)
        from scipy.stats import norm
        if is_call:
            probability = norm.cdf(d1)
        else:
            # For puts, probability is 1 - norm.cdf(d1)
            probability = 1 - norm.cdf(d1)
        
        return probability * 100  # Convert to percentage
        
    except:
        # Fallback calculation
        if is_call:
            if strike > current_price:
                return 30.0  # Rough estimate for OTM calls
            else:
                return 70.0  # Rough estimate for ITM calls
        else:
            if strike < current_price:
                return 30.0  # Rough estimate for OTM puts
            else:
                return 70.0  # Rough estimate for ITM puts

def get_options_data(symbol, volatility, strategy):
    """Get options data for the next two expiration dates"""
    try:
        stock = yf.Ticker(symbol)
        
        # Get options expiration dates
        options = stock.options
        
        if not options:
            return None, "No options data available"
        
        # Get next two expiration dates
        next_two_expirations = options[:2]
        
        options_data = []
        
        for expiration in next_two_expirations:
            try:
                # Get options chain
                opt = stock.option_chain(expiration)
                
                # Get current stock price
                current_price = stock.info.get('currentPrice', 0)
                if current_price == 0:
                    current_price = opt.calls['strike'].iloc[0] if not opt.calls.empty else 100  # Fallback
                
                # Choose calls or puts based on strategy
                if strategy == "calls":
                    options_chain = opt.calls
                    is_call = True
                    # For selling calls, get strikes ABOVE current price (but not too far)
                    # Look for strikes between current_price and current_price * 1.15
                    max_strike = current_price * 1.15
                    filtered_options = options_chain[
                        (options_chain['strike'] > current_price) & 
                        (options_chain['strike'] <= max_strike)
                    ].copy()
                else:  # puts
                    options_chain = opt.puts
                    is_call = False
                    # For selling puts, get strikes BELOW current price but close to it
                    # Look for strikes between current_price * 0.95 and current_price
                    min_strike = current_price * 0.95
                    filtered_options = options_chain[
                        (options_chain['strike'] < current_price) & 
                        (options_chain['strike'] >= min_strike)
                    ].copy()
                
                # Get 10 strike prices
                if len(filtered_options) >= 10:
                    selected_options = filtered_options.head(10).copy()
                else:
                    selected_options = filtered_options.copy()
                
                # Calculate days to expiration
                days_to_expiry = (pd.to_datetime(expiration) - pd.Timestamp.now()).days
                
                # Calculate Greeks and other metrics
                for i, option in selected_options.iterrows():
                    # Delta (approximation)
                    if is_call:
                        delta = 0.5 + (0.5 * (current_price - option['strike']) / (current_price * 0.1))
                    else:
                        delta = -0.5 + (0.5 * (option['strike'] - current_price) / (current_price * 0.1))
                    delta = max(-1, min(1, delta))  # Clamp between -1 and 1
                    
                    # Theta (approximation - time decay)
                    theta = -option['lastPrice'] / (days_to_expiry + 1) if days_to_expiry > 0 else 0
                    
                    # Probability of being ITM
                    probability = calculate_probability_itm(
                        current_price, 
                        option['strike'], 
                        volatility, 
                        days_to_expiry,
                        is_call
                    )
                    
                    # Update the option data using .loc to avoid warnings
                    selected_options.loc[i, 'delta'] = delta
                    selected_options.loc[i, 'theta'] = theta
                    selected_options.loc[i, 'probability'] = probability
                
                options_data.append({
                    'expiration': expiration,
                    'days_to_expiry': days_to_expiry,
                    'options': selected_options.to_dict('records')
                })
                
            except Exception as e:
                print(f"Error getting options for {expiration}: {e}")
                continue
        
        return options_data, None
        
    except Exception as e:
        return None, f"Error getting options: {e}"

def display_results(stock_info, options_data, strategy):
    """Display the results in a nice format"""
    strategy_name = "COVERED CALLS" if strategy == "calls" else "CASH SECURED PUTS"
    
    print("\n" + "="*80)
    print(f"📊 ANALYSIS FOR {stock_info['symbol'].upper()} - {strategy_name}")
    print("="*80)
    
    print(f"\n💰 Current Price: ${stock_info['current_price']:.2f}")
    print(f"📈 Volatility (20-day): {stock_info['volatility']:.1f}%")
    
    if options_data:
        print(f"\n🎯 {strategy_name.upper()} OPPORTUNITIES:")
        print("-" * 70)
        
        for i, exp_data in enumerate(options_data, 1):
            print(f"\n📅 Expiration {i}: {exp_data['expiration']} ({exp_data['days_to_expiry']} days)")
            print("-" * 50)
            
            options = exp_data['options']
            if options:
                print(f"{'Strike':<8} {'Premium':<8} {'Volume':<8} {'OI':<8} {'Delta':<8} {'Theta':<8} {'Prob%':<8}")
                print("-" * 70)
                
                for option in options:
                    strike = option['strike']
                    premium = option['lastPrice']
                    volume = option.get('volume', 0)
                    open_interest = option.get('openInterest', 0)
                    delta = option.get('delta', 0)
                    theta = option.get('theta', 0)
                    probability = option.get('probability', 0)
                    
                    print(f"${strike:<7.2f} ${premium:<7.2f} {volume:<8} {open_interest:<8} {delta:<8.3f} {theta:<8.3f} {probability:<8.1f}")
            else:
                print("No suitable options found")
    else:
        print("\n❌ No options data available")

def main():
    """Main program"""
    print("🚀 Simple Stock Options Analyzer")
    print("="*50)
    print("Choose your strategy and enter stock symbols")
    print("Type 'quit' to exit")
    print("="*50)
    
    while True:
        # Get strategy preference
        print("\n📋 Strategy Options:")
        print("1. Sell Covered Calls (strikes ABOVE current price)")
        print("2. Sell Cash Secured Puts (strikes BELOW current price)")
        
        strategy_choice = input("\n🎯 Choose strategy (1 or 2): ").strip()
        
        if strategy_choice.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        if strategy_choice == "1":
            strategy = "calls"
            strategy_name = "Covered Calls"
        elif strategy_choice == "2":
            strategy = "puts"
            strategy_name = "Cash Secured Puts"
        else:
            print("❌ Please enter 1 or 2")
            continue
        
        # Get stock symbol
        symbol = input(f"\n📈 Enter stock symbol for {strategy_name}: ").strip().upper()
        
        if symbol.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        if not symbol:
            print("❌ Please enter a valid stock symbol")
            continue
        
        print(f"\n🔍 Analyzing {symbol} for {strategy_name}...")
        
        # Get stock data
        stock_info, error = get_stock_data(symbol)
        
        if error:
            print(f"❌ {error}")
            continue
        
        # Get options data
        options_data, options_error = get_options_data(symbol, stock_info['volatility'], strategy)
        
        if options_error:
            print(f"⚠️  {options_error}")
            # Still show stock info even if options fail
            display_results(stock_info, None, strategy)
        else:
            # Display results
            display_results(stock_info, options_data, strategy)
        
        print("\n" + "="*80)

if __name__ == "__main__":
    main() 