import yfinance as yf
import pandas as pd
from typing import Dict, Optional, Any

class StockDataFetcher:
    """Handles fetching stock data from Yahoo Finance"""
    
    def __init__(self):
        self.cache = {}
    
    def get_stock_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        Fetch comprehensive stock information
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            Dictionary containing stock information or None if error
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Validate that we got actual data
            if not info or 'regularMarketPrice' not in info and 'currentPrice' not in info:
                return None
                
            return info
            
        except Exception as e:
            print(f"Error fetching stock info for {symbol}: {e}")
            return None
    
    def get_historical_data(self, symbol: str, period: str = "1y") -> Optional[pd.DataFrame]:
        """
        Fetch historical stock data
        
        Args:
            symbol: Stock ticker symbol
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            
        Returns:
            DataFrame with historical data or None if error
        """
        try:
            ticker = yf.Ticker(symbol)
            hist_data = ticker.history(period=period)
            
            if hist_data.empty:
                return None
                
            # Clean up the data
            hist_data = hist_data.dropna()
            
            # Ensure we have the required columns
            required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            if not all(col in hist_data.columns for col in required_columns):
                return None
                
            return hist_data
            
        except Exception as e:
            print(f"Error fetching historical data for {symbol}: {e}")
            return None
    
    def get_real_time_price(self, symbol: str) -> Optional[float]:
        """
        Get real-time stock price
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            Current stock price or None if error
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d", interval="1m")
            
            if data.empty:
                return None
                
            return float(data['Close'].iloc[-1])
            
        except Exception as e:
            print(f"Error fetching real-time price for {symbol}: {e}")
            return None
    
    def validate_symbol(self, symbol: str) -> bool:
        """
        Validate if a stock symbol exists
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            True if symbol is valid, False otherwise
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Check if we got valid data
            return bool(info and ('regularMarketPrice' in info or 'currentPrice' in info))
            
        except Exception:
            return False
    
    def get_financial_ratios(self, symbol: str) -> Optional[Dict[str, float]]:
        """
        Calculate and return key financial ratios
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            Dictionary containing financial ratios
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            if not info:
                return None
                
            ratios = {
                'pe_ratio': info.get('trailingPE'),
                'forward_pe': info.get('forwardPE'),
                'peg_ratio': info.get('pegRatio'),
                'price_to_book': info.get('priceToBook'),
                'price_to_sales': info.get('priceToSalesTrailing12Months'),
                'debt_to_equity': info.get('debtToEquity'),
                'return_on_equity': info.get('returnOnEquity'),
                'return_on_assets': info.get('returnOnAssets'),
                'profit_margin': info.get('profitMargins'),
                'operating_margin': info.get('operatingMargins'),
                'gross_margin': info.get('grossMargins')
            }
            
            # Filter out None values
            return {k: v for k, v in ratios.items() if v is not None}
            
        except Exception as e:
            print(f"Error calculating financial ratios for {symbol}: {e}")
            return None
