# Global Stock Analysis & Trading Dashboard

## Overview

This is a comprehensive Streamlit-based stock analysis and trading simulation platform that provides real-time stock data visualization, technical analysis, and paper trading capabilities. The application covers global markets including US, Indian, UK, German, Japanese, Chinese, Canadian, Australian, and Brazilian stocks. It features advanced technical indicators, real-time buy/sell signals, and an integrated trading simulator for risk-free practice trading.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a simple three-tier architecture:

1. **Presentation Layer**: Streamlit web interface (`app.py`)
2. **Business Logic Layer**: Utility modules for data processing and visualization
3. **Data Layer**: Yahoo Finance API integration for real-time stock data

The architecture emphasizes modularity and separation of concerns, with distinct components for data fetching and chart generation.

## Key Components

### Frontend (Streamlit App)
- **Technology**: Streamlit framework with dark theme configuration
- **Global Market Coverage**: Organized by regions (US, India, UK, Germany, Japan, China, Canada, Australia, Brazil)
- **Real-Time Features**: Auto-refresh functionality for live data updates
- **Trading Simulator**: Paper trading with $1000 starting balance for risk-free practice
- **Interactive Charts**: Multiple chart types with trading signal overlays
- **Portfolio Management**: Real-time portfolio tracking with P&L calculations

### Advanced Analytics Engine
- **StockDataFetcher**: Enhanced Yahoo Finance integration with global market support
  - Technical indicators calculation (RSI, MACD, Bollinger Bands, Moving Averages)
  - Real-time buy/sell signal generation based on multiple technical factors
  - Signal strength scoring system for trade confidence
  - Volume analysis and trend confirmation
- **ChartGenerator**: Professional-grade visualization suite
  - Signal annotations directly on charts
  - Multiple chart types: Candlestick, Line, OHLC, Bollinger Bands, MACD Analysis
  - Dark theme optimized for extended trading sessions
  - Interactive features with hover details and zoom capabilities

### Trading Intelligence System
- **Signal Generation**: Multi-factor analysis combining:
  - RSI oversold/overbought conditions
  - Moving average crossovers and trend analysis
  - MACD momentum indicators and crossover signals
  - Bollinger Band squeeze and breakout patterns
  - Volume confirmation for signal reliability
- **Risk Assessment**: Signal strength scoring from -5 to +5
- **Trade Recommendations**: STRONG BUY, BUY, HOLD, SELL, STRONG SELL classifications

### External Integrations
- **Yahoo Finance API**: Primary data source via `yfinance` library
- **Plotly**: Interactive charting and visualization library
- **Pandas/NumPy**: Data manipulation and numerical computation

## Data Flow

1. User inputs stock symbol and time period through Streamlit sidebar
2. StockDataFetcher validates input and retrieves data from Yahoo Finance
3. Data is processed and cached in session state
4. ChartGenerator creates visualizations based on fetched data
5. Charts and metrics are displayed in the main Streamlit interface

## External Dependencies

- **yfinance**: Yahoo Finance API wrapper for stock data retrieval
- **streamlit**: Web application framework
- **plotly**: Interactive visualization library
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing support

## Deployment Strategy

The application is designed for simple deployment scenarios:

- **Local Development**: Direct execution via `streamlit run app.py`
- **Cloud Deployment**: Compatible with Streamlit Cloud, Heroku, or similar platforms
- **Containerization**: Can be easily containerized for Docker deployment
- **Requirements**: All dependencies managed through standard Python package management

### Architectural Decisions

**Problem**: Need for real-time stock data visualization
**Solution**: Yahoo Finance API integration with Streamlit frontend
**Rationale**: Yahoo Finance provides reliable, free stock data, while Streamlit enables rapid development of interactive web applications

**Problem**: Maintaining clean, modular code structure
**Solution**: Separation of concerns with dedicated utility modules
**Rationale**: Improves maintainability and testability while enabling code reuse

**Problem**: Creating professional-looking visualizations
**Solution**: Plotly with custom dark theme implementation
**Rationale**: Plotly provides interactive charts with professional appearance, dark theme reduces eye strain during extended use

**Problem**: Managing API rate limits and performance
**Solution**: Basic caching implementation in data fetcher
**Rationale**: Reduces redundant API calls and improves application responsiveness