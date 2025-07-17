"""
Configuration settings for the trading application
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration"""
    
    # Database configuration
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///trading_app.db')
    
    # Application settings
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    NEWS_API_KEY = os.getenv('NEWS_API_KEY')
    
    # Streamlit configuration
    STREAMLIT_CONFIG = {
        'server.port': int(os.getenv('PORT', 8501)),
        'server.address': '0.0.0.0',
        'server.headless': True,
        'server.enableCORS': False,
        'server.enableXsrfProtection': False
    }
    
    # Trading simulation settings
    INITIAL_BALANCE = 10000.0
    MAX_POSITION_SIZE = 0.35  # 35% of portfolio
    
    # Data refresh intervals (in seconds)
    PRICE_REFRESH_INTERVAL = 60
    NEWS_REFRESH_INTERVAL = 300  # 5 minutes
    
    # Feature flags
    ENABLE_NEWS_SENTIMENT = True
    ENABLE_BACKTESTING = True
    ENABLE_ML_FEATURES = True
    ENABLE_REAL_TIME_LEARNING = True

# Create config instance
config = Config()