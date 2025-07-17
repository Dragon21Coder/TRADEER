# SUDNAXI - Professional AI Trading Intelligence Platform

A comprehensive, production-ready stock trading analysis platform featuring advanced machine learning, real-time market data, and professional-grade analytics. Built with modern Python technologies for institutional-level trading intelligence.

## Features

### Core Trading Intelligence
- **Real-time Market Data**: Live stock prices from global markets (US, India, UK, Germany, Japan, China, Canada, Australia, Brazil)
- **Advanced Technical Analysis**: RSI, MACD, Bollinger Bands, Moving Averages, Volume Analysis
- **AI-Powered Signal Generation**: Multi-factor analysis with confidence scoring (-5 to +5)
- **Smart Trading Recommendations**: STRONG BUY, BUY, HOLD, SELL, STRONG SELL classifications

### Professional Analytics
- **Machine Learning Backtesting**: Generate 1000+ trades with optimized strategies
- **News Sentiment Analysis**: Real-time news integration with sentiment scoring
- **Buy/Sell Ratio Analysis**: Analyst recommendations and price target analysis
- **Portfolio Simulation**: Paper trading with $10,000 starting balance
- **Risk Management**: Advanced position sizing and risk assessment

### Advanced Features
- **Adaptive AI Strategies**: Real-time learning with 30-minute adaptation cycles
- **Continuous Learning Engine**: Strategy enhancement based on performance
- **Professional UI/UX**: Dark theme optimized for extended trading sessions
- **Interactive Charts**: Multiple chart types with signal overlays
- **Comprehensive Help System**: Educational tooltips and trading insights

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or Download** the project files to your local machine

2. **Install Dependencies**:
   ```bash
   pip install -r production_requirements.txt
   ```

3. **Configure Environment** (Optional):
   ```bash
   cp .env.example .env
   # Edit .env with your configurations
   ```

4. **Run the Application**:
   ```bash
   python run_production.py
   ```

   Or directly with Streamlit:
   ```bash
   streamlit run app.py --server.port=8501
   ```

5. **Access the Platform**:
   Open your browser and navigate to `http://localhost:8501`

## Configuration

### Environment Variables
Create a `.env` file in the root directory with the following configurations:

```env
# Database (Optional - defaults to SQLite)
DATABASE_URL=sqlite:///./trading_app.db

# Application Settings
DEBUG=False
ENVIRONMENT=production

# Optional API Keys
OPENAI_API_KEY=your_openai_key_here
NEWS_API_KEY=your_news_api_key_here
```

### Database Options
- **SQLite** (Default): No additional setup required
- **PostgreSQL**: Set `DATABASE_URL=postgresql://user:password@localhost:5432/trading_db`

## Docker Deployment

### Using Docker Compose (Recommended)
```bash
docker-compose up -d
```

### Manual Docker Build
```bash
docker build -t sudnaxi-trading .
docker run -p 8501:8501 sudnaxi-trading
```

## Project Structure

```
sudnaxi-trading/
├── app.py                      # Main Streamlit application
├── config.py                   # Application configuration
├── run_production.py           # Production launcher
├── production_requirements.txt # Python dependencies
├── .env.example               # Environment template
├── database/
│   └── models.py              # Database models
├── ml/
│   ├── adaptive_strategy.py   # ML trading strategies
│   └── reinforcement_learning.py # RL components
├── utils/
│   ├── data_fetcher.py        # Market data retrieval
│   ├── chart_generator.py     # Chart visualization
│   ├── news_sentiment.py      # News analysis
│   ├── backtesting_engine.py  # Strategy testing
│   └── enhanced_backtesting.py # Advanced backtesting
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose setup
└── README.md                  # This file
```

## Technology Stack

- **Backend**: Python 3.8+, SQLAlchemy, Pandas, NumPy
- **Frontend**: Streamlit with custom dark theme
- **Data Sources**: Yahoo Finance API, Real-time news feeds
- **Machine Learning**: scikit-learn, TensorFlow (optional)
- **Visualization**: Plotly with interactive charts
- **Database**: SQLite (default), PostgreSQL (optional)

## Features Overview

### Trading Analysis
- Multi-timeframe analysis (1D, 5D, 1M, 3M, 6M, 1Y, 2Y, 5Y)
- Global market coverage with 500+ stocks
- Real-time price updates and alerts
- Technical indicator calculations
- Volume and trend analysis

### Machine Learning
- Adaptive strategy optimization
- Performance-based learning cycles
- Signal strength enhancement
- Risk-adjusted position sizing
- Backtesting with 1000+ trade generation

### User Interface
- Professional dark theme
- Interactive charts with zoom and hover
- Real-time data refresh
- Comprehensive help tooltips
- Mobile-responsive design

## Performance Optimization

- **Caching**: Intelligent data caching for improved performance
- **Async Processing**: Background data updates
- **Memory Management**: Efficient data handling for large datasets
- **API Rate Limiting**: Optimized API calls to prevent throttling

## Security Features

- Environment-based configuration
- API key management
- Secure database connections
- Input validation and sanitization
- Error handling and logging

## Development

### Local Development Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r production_requirements.txt

# Run in development mode
streamlit run app.py
```

### Adding New Features
1. Create feature branch
2. Implement functionality in appropriate module
3. Update configuration if needed
4. Test thoroughly
5. Update documentation

## Troubleshooting

### Common Issues

**Database Connection Error**:
- Check DATABASE_URL in .env file
- Ensure database server is running
- Verify connection credentials

**API Rate Limiting**:
- Reduce refresh frequency
- Check API key quotas
- Implement caching strategies

**Memory Issues**:
- Reduce data timeframes
- Clear browser cache
- Restart application

**Installation Problems**:
- Update pip: `pip install --upgrade pip`
- Install build tools: `pip install wheel setuptools`
- Use virtual environment

## License

MIT License - See LICENSE file for details

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## Support

For issues and questions:
- Check troubleshooting section
- Review configuration settings
- Verify API connections
- Check system requirements

---

**SUDNAXI Trading Platform** - Professional AI-Powered Trading Intelligence