#!/usr/bin/env python3
"""
Test script to verify installation and basic functionality
"""

import sys
import importlib

def test_imports():
    """Test that all required packages can be imported"""
    print("Testing imports...")
    
    required_packages = [
        'yfinance',
        'pandas',
        'numpy',
        'requests',
        'streamlit',
        'plotly',
        'sklearn',
        'ta'
    ]
    
    failed_imports = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package}: {e}")
            failed_imports.append(package)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        print("Please install missing packages with: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All imports successful!")
        return True

def test_basic_functionality():
    """Test basic functionality"""
    print("\nTesting basic functionality...")
    
    try:
        from stock_analyzer import StockAnalyzer
        from stock_screener import StockScreener
        
        print("✅ Custom modules imported successfully")
        
        # Test analyzer initialization
        analyzer = StockAnalyzer()
        print("✅ StockAnalyzer initialized")
        
        # Test screener initialization
        screener = StockScreener()
        print("✅ StockScreener initialized")
        
        # Test getting popular stocks
        popular_stocks = screener.get_popular_stocks()
        print(f"✅ Retrieved {len(popular_stocks)} popular stocks")
        
        # Test getting high volume stocks
        high_volume_stocks = screener.get_high_volume_stocks()
        print(f"✅ Retrieved {len(high_volume_stocks)} high volume stocks")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def test_data_access():
    """Test data access from Yahoo Finance"""
    print("\nTesting data access...")
    
    try:
        import yfinance as yf
        
        # Test basic stock data
        aapl = yf.Ticker("AAPL")
        info = aapl.info
        
        if info.get('currentPrice'):
            print("✅ Yahoo Finance data access successful")
            return True
        else:
            print("❌ Could not retrieve stock data")
            return False
            
    except Exception as e:
        print(f"❌ Data access test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Stock Call Options Recommender - Installation Test")
    print("=" * 60)
    
    # Test imports
    imports_ok = test_imports()
    
    if not imports_ok:
        print("\n❌ Installation test failed - missing dependencies")
        return False
    
    # Test basic functionality
    functionality_ok = test_basic_functionality()
    
    if not functionality_ok:
        print("\n❌ Installation test failed - basic functionality error")
        return False
    
    # Test data access
    data_ok = test_data_access()
    
    if not data_ok:
        print("\n❌ Installation test failed - data access error")
        return False
    
    print("\n" + "=" * 60)
    print("✅ All tests passed! Installation successful.")
    print("=" * 60)
    print("\n🚀 You can now run the application with:")
    print("   streamlit run app.py")
    print("\n📊 Or run the demo with:")
    print("   python run_demo.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 