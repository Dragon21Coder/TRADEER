"""
Application configuration and settings
"""
import os
from typing import Dict, Any

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class AppConfig:
    """Application configuration management"""
    
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL', 'sqlite:///./trading_app.db')
        self.debug = os.getenv('DEBUG', 'False').lower() == 'true'
        self.environment = os.getenv('ENVIRONMENT', 'production')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.news_api_key = os.getenv('NEWS_API_KEY')
        
        # Trading settings
        self.initial_balance = float(os.getenv('INITIAL_BALANCE', '10000.0'))
        self.max_position_size = float(os.getenv('MAX_POSITION_SIZE', '0.35'))
        
        # Server settings
        self.port = int(os.getenv('PORT', '8501'))
        self.host = os.getenv('HOST', '0.0.0.0')
        
        # Feature flags
        self.enable_news_sentiment = os.getenv('ENABLE_NEWS_SENTIMENT', 'true').lower() == 'true'
        self.enable_backtesting = os.getenv('ENABLE_BACKTESTING', 'true').lower() == 'true'
        self.enable_ml_features = os.getenv('ENABLE_ML_FEATURES', 'true').lower() == 'true'
    
    def get_streamlit_config(self) -> Dict[str, Any]:
        """Get Streamlit configuration"""
        return {
            'server.port': self.port,
            'server.address': self.host,
            'server.headless': True,
            'server.enableCORS': False,
            'server.enableXsrfProtection': False
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            'database_url': self.database_url,
            'debug': self.debug,
            'environment': self.environment,
            'initial_balance': self.initial_balance,
            'max_position_size': self.max_position_size,
            'port': self.port,
            'host': self.host,
            'enable_news_sentiment': self.enable_news_sentiment,
            'enable_backtesting': self.enable_backtesting,
            'enable_ml_features': self.enable_ml_features
        }

# Global configuration instance
config = AppConfig()