import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import time
from utils.data_fetcher import StockDataFetcher
from utils.chart_generator import ChartGenerator
from utils.news_sentiment import NewsSentimentAnalyzer
from utils.backtesting_engine import BacktestingEngine

# Configure page
st.set_page_config(
    page_title="Global Stock Analysis & Trading Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional UI
st.markdown("""
<style>
/* Main container styling */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 100%;
}

/* Metric cards styling */
[data-testid="metric-container"] {
    background-color: #262730;
    border: 1px solid #404040;
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Headers styling */
h1, h2, h3 {
    color: #FAFAFA;
    font-weight: 600;
}

/* Button styling */
.stButton > button {
    background: linear-gradient(45deg, #00FF88, #00CC70);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background: linear-gradient(45deg, #00CC70, #00AA5C);
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,255,136,0.3);
}

/* Selectbox styling */
.stSelectbox > div > div {
    background-color: #262730;
    border: 1px solid #404040;
    border-radius: 8px;
}

/* Info box styling */
.stInfo {
    background-color: #1a3a4a;
    border-left: 4px solid #00FF88;
    padding: 1rem;
    border-radius: 8px;
}

/* Success box styling */
.stSuccess {
    background-color: #1a4a2a;
    border-left: 4px solid #00FF88;
    padding: 1rem;
    border-radius: 8px;
}

/* Warning box styling */
.stWarning {
    background-color: #4a3a1a;
    border-left: 4px solid #FFD700;
    padding: 1rem;
    border-radius: 8px;
}

/* Expander styling */
.streamlit-expanderHeader {
    background-color: #262730;
    border-radius: 8px;
    border: 1px solid #404040;
}

/* Chart container styling */
.stPlotlyChart {
    background-color: #262730;
    border-radius: 10px;
    padding: 1rem;
    border: 1px solid #404040;
}

/* Professional section dividers */
hr {
    border: none;
    height: 2px;
    background: linear-gradient(90deg, transparent, #00FF88, transparent);
    margin: 2rem 0;
}

/* Card-like containers */
.metric-card {
    background: linear-gradient(135deg, #262730 0%, #2a2a3a 100%);
    border-radius: 12px;
    padding: 1.5rem;
    border: 1px solid #404040;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'stock_data' not in st.session_state:
    st.session_state.stock_data = None
if 'current_symbol' not in st.session_state:
    st.session_state.current_symbol = ""

def main():
    # Professional title header
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #262730 0%, #1a1a2e 100%); border-radius: 15px; margin-bottom: 2rem; border: 1px solid #404040;">
        <h1 style="color: #00FF88; font-size: 3rem; margin: 0; text-shadow: 0 0 10px rgba(0,255,136,0.3);">🌍 Global Stock Analysis</h1>
        <h2 style="color: #FAFAFA; font-size: 1.5rem; margin: 0.5rem 0 0 0; font-weight: 300;">Professional Trading Dashboard</h2>
        <p style="color: #CCCCCC; margin: 0.5rem 0 0 0;">Real-time data • Technical indicators • News sentiment • Backtesting • Trading simulation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Important disclaimer
    with st.expander("⚠️ Important Disclaimer - READ BEFORE USING", expanded=False):
        st.warning("""
        **EDUCATIONAL PURPOSE ONLY - NOT INVESTMENT ADVICE**
        
        This application is designed for educational purposes and trading simulation only. Please note:
        
        🚨 **Trading Simulation Only**: This app provides a paper trading simulator, not real trading capabilities
        
        📊 **No Real Money**: All trades are simulated with virtual money for learning purposes
        
        ⚡ **Data Limitations**: Yahoo Finance free API has limitations - real trading requires premium data feeds
        
        🎯 **Educational Tool**: Use this to learn technical analysis and practice trading strategies risk-free
        
        💼 **Investment Advice**: This is NOT professional investment advice. Always consult qualified financial advisors
        
        🔒 **Risk Warning**: Real trading involves significant financial risk. Never invest more than you can afford to lose
        
        **For Real Trading**: Use licensed brokers with proper risk management, real-time data, and professional tools
        """)
    
    st.markdown("---")
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("Stock Selection")
        
        # Global stock symbols organized by region
        stock_regions = {
            "🇺🇸 US Stocks": {
                "Apple Inc. (AAPL)": "AAPL",
                "Microsoft Corp. (MSFT)": "MSFT", 
                "Amazon.com Inc. (AMZN)": "AMZN",
                "Tesla Inc. (TSLA)": "TSLA",
                "Alphabet Inc. (GOOGL)": "GOOGL",
                "Meta Platforms (META)": "META",
                "NVIDIA Corp. (NVDA)": "NVDA",
                "Netflix Inc. (NFLX)": "NFLX",
                "Berkshire Hathaway (BRK-B)": "BRK-B",
                "Johnson & Johnson (JNJ)": "JNJ",
                "JPMorgan Chase (JPM)": "JPM",
                "Visa Inc. (V)": "V"
            },
            "🇮🇳 Indian Stocks": {
                "Reliance Industries (RELIANCE.NS)": "RELIANCE.NS",
                "Tata Consultancy Services (TCS.NS)": "TCS.NS",
                "HDFC Bank (HDFCBANK.NS)": "HDFCBANK.NS",
                "Infosys (INFY.NS)": "INFY.NS",
                "ICICI Bank (ICICIBANK.NS)": "ICICIBANK.NS",
                "State Bank of India (SBIN.NS)": "SBIN.NS",
                "Bharti Airtel (BHARTIARTL.NS)": "BHARTIARTL.NS",
                "ITC Ltd (ITC.NS)": "ITC.NS",
                "Hindustan Unilever (HINDUNILVR.NS)": "HINDUNILVR.NS",
                "Larsen & Toubro (LT.NS)": "LT.NS"
            },
            "🇬🇧 UK Stocks": {
                "Royal Dutch Shell (SHEL.L)": "SHEL.L",
                "AstraZeneca (AZN.L)": "AZN.L",
                "British Petroleum (BP.L)": "BP.L",
                "HSBC Holdings (HSBA.L)": "HSBA.L",
                "Vodafone Group (VOD.L)": "VOD.L",
                "Rio Tinto (RIO.L)": "RIO.L",
                "Unilever (ULVR.L)": "ULVR.L",
                "BT Group (BT-A.L)": "BT-A.L"
            },
            "🇩🇪 German Stocks": {
                "SAP SE (SAP.DE)": "SAP.DE",
                "Siemens AG (SIE.DE)": "SIE.DE",
                "ASML Holding (ASML.AS)": "ASML.AS",
                "Allianz SE (ALV.DE)": "ALV.DE",
                "Deutsche Bank (DBK.DE)": "DBK.DE",
                "BMW AG (BMW.DE)": "BMW.DE",
                "Volkswagen (VOW3.DE)": "VOW3.DE"
            },
            "🇯🇵 Japanese Stocks": {
                "Toyota Motor (7203.T)": "7203.T",
                "Sony Group (6758.T)": "6758.T",
                "SoftBank Group (9984.T)": "9984.T",
                "Nintendo (7974.T)": "7974.T",
                "Honda Motor (7267.T)": "7267.T",
                "Mitsubishi UFJ (8306.T)": "8306.T"
            },
            "🇨🇳 Chinese Stocks": {
                "Alibaba Group (BABA)": "BABA",
                "Tencent Holdings (0700.HK)": "0700.HK",
                "Taiwan Semiconductor (TSM)": "TSM",
                "JD.com (JD)": "JD",
                "Baidu Inc (BIDU)": "BIDU",
                "NetEase Inc (NTES)": "NTES"
            },
            "🇨🇦 Canadian Stocks": {
                "Shopify Inc (SHOP.TO)": "SHOP.TO",
                "Royal Bank of Canada (RY.TO)": "RY.TO",
                "Canadian National Railway (CNR.TO)": "CNR.TO",
                "Brookfield Asset Management (BAM.TO)": "BAM.TO"
            },
            "🇦🇺 Australian Stocks": {
                "BHP Group (BHP.AX)": "BHP.AX",
                "Commonwealth Bank (CBA.AX)": "CBA.AX",
                "CSL Limited (CSL.AX)": "CSL.AX",
                "Westpac Banking (WBC.AX)": "WBC.AX"
            },
            "🇧🇷 Brazilian Stocks": {
                "Petrobras (PETR4.SA)": "PETR4.SA",
                "Vale SA (VALE3.SA)": "VALE3.SA",
                "Itau Unibanco (ITUB4.SA)": "ITUB4.SA",
                "Banco do Brasil (BBAS3.SA)": "BBAS3.SA"
            }
        }
        
        # Region selection
        selected_region = st.selectbox(
            "Select Market Region",
            options=list(stock_regions.keys()),
            index=0
        )
        
        popular_stocks = stock_regions[selected_region]
        
        # Stock selection dropdown
        selected_stock_display = st.selectbox(
            "Select a Stock",
            options=list(popular_stocks.keys()),
            index=0,
            help="Choose from popular, reliable stock symbols"
        )
        stock_symbol = popular_stocks[selected_stock_display]
        
        # Manual input option
        st.subheader("Or Enter Custom Symbol")
        custom_symbol = st.text_input(
            "Custom Stock Symbol",
            placeholder="e.g., AAPL, MSFT",
            help="Enter any valid stock ticker symbol"
        ).upper()
        
        if custom_symbol:
            stock_symbol = custom_symbol
        
        # Time period selection
        time_periods = {
            "1 Week": "1wk",
            "1 Month": "1mo", 
            "3 Months": "3mo",
            "6 Months": "6mo",
            "1 Year": "1y",
            "2 Years": "2y",
            "5 Years": "5y"
        }
        
        selected_period = st.selectbox(
            "Time Period",
            options=list(time_periods.keys()),
            index=4  # Default to 1 Year
        )
        
        # Chart type selection
        chart_types = ["Candlestick", "Line", "OHLC", "Bollinger Bands", "MACD Analysis"]
        chart_type = st.selectbox("Chart Type", chart_types)
        
        # Real-time options
        st.subheader("📡 Real-Time Features")
        auto_refresh = st.checkbox("🔄 Auto-refresh every 15 seconds", value=False)
        show_news = st.checkbox("📰 Show News Sentiment", value=True)
        show_backtest = st.checkbox("📊 Show Backtesting Results", value=True)
        
        # Trading simulator toggle
        trading_mode = st.checkbox("Enable Trading Simulator", value=False)
        
        if trading_mode:
            st.subheader("💰 Trading Simulator")
            if 'portfolio_balance' not in st.session_state:
                st.session_state.portfolio_balance = 1000.0  # Starting with $1000
            if 'portfolio_holdings' not in st.session_state:
                st.session_state.portfolio_holdings = {}
            
            st.metric("Portfolio Balance", f"${st.session_state.portfolio_balance:.2f}")
            
            # Investment amount
            investment_amount = st.number_input(
                "Investment Amount ($)", 
                min_value=1.0, 
                max_value=float(st.session_state.portfolio_balance),
                value=min(100.0, st.session_state.portfolio_balance),
                step=1.0
            )
        
        # Fetch data button
        fetch_button = st.button("Fetch Stock Data", type="primary")
        
        # Real-time refresh interval selector
        if auto_refresh:
            refresh_interval = st.selectbox(
                "Refresh Interval",
                options=[5, 10, 15, 30, 60],
                index=2,
                format_func=lambda x: f"{x} seconds"
            )
    
    # Main content area
    if fetch_button or (stock_symbol and stock_symbol != st.session_state.current_symbol):
        if stock_symbol:
            with st.spinner(f"Fetching data for {stock_symbol}..."):
                try:
                    # Initialize data fetcher
                    fetcher = StockDataFetcher()
                    
                    # Fetch stock data
                    stock_info = fetcher.get_stock_info(stock_symbol)
                    historical_data = fetcher.get_historical_data(
                        stock_symbol, 
                        time_periods[selected_period]
                    )
                    
                    if stock_info and historical_data is not None and not historical_data.empty:
                        # Calculate technical indicators
                        historical_data_with_indicators = fetcher.calculate_technical_indicators(historical_data.copy())
                        
                        # Generate buy/sell signals
                        trading_signal = fetcher.generate_buy_sell_signal(historical_data_with_indicators)
                        
                        # Fetch news sentiment if enabled
                        news_data = None
                        sentiment_summary = None
                        if show_news:
                            try:
                                with st.spinner("🔄 Analyzing news sentiment..."):
                                    news_analyzer = NewsSentimentAnalyzer()
                                    news_data = news_analyzer.get_stock_news(stock_symbol, limit=15)
                                    sentiment_summary = news_analyzer.get_overall_sentiment(news_data)
                                    st.success(f"✅ Analyzed {len(news_data)} news articles for sentiment")
                            except Exception as e:
                                st.warning(f"News analysis temporarily unavailable: {e}")
                                # Provide fallback data to ensure UI works
                                news_data = [{
                                    'title': f"{stock_symbol} Market Analysis",
                                    'summary': f"Technical analysis shows current trading signals and market trends for {stock_symbol}.",
                                    'link': '',
                                    'published': datetime.now().strftime("%Y-%m-%d %H:%M"),
                                    'source': 'Trading Platform',
                                    'sentiment_score': 0.0,
                                    'sentiment_label': 'Neutral',
                                    'relevance': 0.8
                                }]
                                sentiment_summary = news_analyzer.get_overall_sentiment(news_data)
                        
                        # Run backtesting if enabled
                        backtest_results = None
                        if show_backtest:
                            try:
                                backtesting_engine = BacktestingEngine()
                                backtest_results = backtesting_engine.run_backtest(stock_symbol, "1y", 10000)
                            except Exception as e:
                                st.warning(f"Could not run backtesting: {e}")
                        
                        st.session_state.stock_data = {
                            'info': stock_info,
                            'historical': historical_data_with_indicators,
                            'symbol': stock_symbol,
                            'period': selected_period,
                            'trading_signal': trading_signal,
                            'news_data': news_data,
                            'sentiment_summary': sentiment_summary,
                            'backtest_results': backtest_results,
                            'last_updated': datetime.now()
                        }
                        st.session_state.current_symbol = stock_symbol
                        st.success(f"✅ Successfully loaded comprehensive data for {stock_symbol}")
                    else:
                        st.error(f"No data found for symbol '{stock_symbol}'. Please check the symbol and try again.")
                        st.session_state.stock_data = None
                        
                except Exception as e:
                    st.error(f"Error fetching data: {str(e)}")
                    st.session_state.stock_data = None
        else:
            st.warning("Please enter a stock symbol")
    
    # Auto-refresh logic
    if auto_refresh and 'stock_data' in st.session_state and st.session_state.stock_data:
        # Create a placeholder for countdown
        countdown_placeholder = st.empty()
        
        # Countdown timer
        for remaining in range(refresh_interval, 0, -1):
            countdown_placeholder.info(f"🔄 Auto-refresh in {remaining} seconds...")
            time.sleep(1)
        
        countdown_placeholder.empty()
        st.rerun()
    
    # Display data if available
    if st.session_state.stock_data:
        display_stock_analysis(chart_type)
    else:
        # Welcome message
        st.info("👆 Enter a stock symbol in the sidebar to get started!")
        
        # Sample symbols
        st.subheader("Popular Stock Symbols")
        col1, col2, col3, col4 = st.columns(4)
        
        sample_symbols = [
            ("AAPL", "Apple Inc."),
            ("GOOGL", "Alphabet Inc."),
            ("MSFT", "Microsoft Corp."),
            ("TSLA", "Tesla Inc."),
            ("AMZN", "Amazon.com Inc."),
            ("META", "Meta Platforms"),
            ("NVDA", "NVIDIA Corp."),
            ("NFLX", "Netflix Inc.")
        ]
        
        for i, (symbol, name) in enumerate(sample_symbols):
            col = [col1, col2, col3, col4][i % 4]
            with col:
                if st.button(f"{symbol}\n{name}", key=f"sample_{symbol}"):
                    st.session_state.current_symbol = symbol
                    st.rerun()

def display_stock_analysis(chart_type):
    """Display the complete stock analysis"""
    data = st.session_state.stock_data
    stock_info = data['info']
    historical_data = data['historical']
    symbol = data['symbol']
    
    # Trading Signal Section (prominently displayed)
    trading_signal = data.get('trading_signal', {})
    signal_color_map = {
        'green': '#00FF88',
        'lightgreen': '#90EE90', 
        'yellow': '#FFD700',
        'orange': '#FFA500',
        'red': '#FF4444',
        'gray': '#888888'
    }
    
    st.markdown("---")
    col_signal, col_strength = st.columns([2, 1])
    
    with col_signal:
        signal_color = signal_color_map.get(trading_signal.get('color', 'gray'), '#888888')
        st.markdown(
            f"<div style='padding: 20px; background-color: {signal_color}20; border-left: 5px solid {signal_color}; border-radius: 5px;'>"
            f"<h2 style='color: {signal_color}; margin: 0;'>🚨 TRADING SIGNAL: {trading_signal.get('signal', 'UNKNOWN')}</h2>"
            f"<p style='margin: 5px 0; color: #FAFAFA;'>Signal Strength: {trading_signal.get('strength', 0):.1f}</p>"
            f"</div>", 
            unsafe_allow_html=True
        )
    
    with col_strength:
        if trading_signal.get('rsi') is not None:
            st.metric(
                label="RSI", 
                value=f"{trading_signal['rsi']:.1f}",
                help="RSI below 30 = oversold, above 70 = overbought"
            )
    
    # Signal reasons
    if trading_signal.get('reasons'):
        st.subheader("📋 Signal Analysis")
        for reason in trading_signal['reasons']:
            st.write(f"• {reason}")
    
    # News Sentiment Analysis Section
    if data.get('news_data') and data.get('sentiment_summary'):
        st.markdown("---")
        
        # Professional section header
        st.markdown("""
        <div style="background: linear-gradient(135deg, #262730 0%, #1a1a2e 100%); border-radius: 12px; padding: 1.5rem; margin: 1rem 0; border: 1px solid #404040;">
            <h2 style="color: #00FF88; margin: 0; display: flex; align-items: center;">
                📰 News Sentiment Analysis
                <span style="margin-left: auto; font-size: 0.8rem; color: #CCCCCC;">Real-time Market Intelligence</span>
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        sentiment_summary = data['sentiment_summary']
        news_data = data['news_data']
        
        # Overall sentiment display with enhanced cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            sentiment_color = "#00FF88" if sentiment_summary['overall_score'] > 0 else "#FF4444" if sentiment_summary['overall_score'] < 0 else "#FFD700"
            st.markdown(
                f"""
                <div class="metric-card" style="text-align: center; background: linear-gradient(135deg, {sentiment_color}20 0%, {sentiment_color}10 100%);">
                    <h3 style="color: {sentiment_color}; margin: 0; font-size: 1.5rem;">{sentiment_summary['overall_label']}</h3>
                    <p style="margin: 0.5rem 0 0 0; color: #FAFAFA; font-size: 1.2rem;">Score: {sentiment_summary['overall_score']:.3f}</p>
                    <small style="color: #CCCCCC;">Overall Market Sentiment</small>
                </div>
                """, 
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                f"""
                <div class="metric-card" style="text-align: center;">
                    <h3 style="color: #00FF88; margin: 0; font-size: 2rem;">{sentiment_summary['positive_count']}</h3>
                    <p style="margin: 0.5rem 0 0 0; color: #FAFAFA;">Positive News</p>
                    <small style="color: #CCCCCC;">Bullish sentiment articles</small>
                </div>
                """, 
                unsafe_allow_html=True
            )
        
        with col3:
            st.markdown(
                f"""
                <div class="metric-card" style="text-align: center;">
                    <h3 style="color: #FF4444; margin: 0; font-size: 2rem;">{sentiment_summary['negative_count']}</h3>
                    <p style="margin: 0.5rem 0 0 0; color: #FAFAFA;">Negative News</p>
                    <small style="color: #CCCCCC;">Bearish sentiment articles</small>
                </div>
                """, 
                unsafe_allow_html=True
            )
        
        with col4:
            st.markdown(
                f"""
                <div class="metric-card" style="text-align: center;">
                    <h3 style="color: #00FF88; margin: 0; font-size: 2rem;">{sentiment_summary['total_articles']}</h3>
                    <p style="margin: 0.5rem 0 0 0; color: #FAFAFA;">Total Articles</p>
                    <small style="color: #CCCCCC;">News sources analyzed</small>
                </div>
                """, 
                unsafe_allow_html=True
            )
        
        # News impact assessment with enhanced styling
        if sentiment_summary['overall_score'] != 0:
            from utils.news_sentiment import NewsSentimentAnalyzer
            analyzer = NewsSentimentAnalyzer()
            impact_assessment = analyzer.get_sentiment_impact_on_price(sentiment_summary['overall_score'])
            
            impact_color = impact_assessment['color']
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, {impact_color}20 0%, {impact_color}10 100%); border-left: 4px solid {impact_color}; border-radius: 10px; padding: 1.5rem; margin: 1rem 0;">
                    <h4 style="color: {impact_color}; margin: 0;">📊 Market Impact Assessment</h4>
                    <p style="margin: 0.5rem 0 0 0; color: #FAFAFA; font-size: 1.1rem;">{impact_assessment['expected_movement']}</p>
                    <small style="color: #CCCCCC;">Confidence Level: {impact_assessment['confidence']:.0f}%</small>
                </div>
                """, 
                unsafe_allow_html=True
            )
        
        # Recent news articles with enhanced display
        st.markdown("""
        <div style="background: linear-gradient(135deg, #262730 0%, #1a1a2e 100%); border-radius: 12px; padding: 1rem; margin: 1rem 0; border: 1px solid #404040;">
            <h3 style="color: #00FF88; margin: 0;">📄 Recent News Articles</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if news_data:
            for i, article in enumerate(news_data[:5]):  # Show top 5 articles
                # Enhanced expander with professional styling
                title_display = f"{article['title'][:80]}..." if len(article['title']) > 80 else article['title']
                
                with st.expander(f"📰 {title_display}", expanded=False):
                    col_content, col_sentiment = st.columns([3, 1])
                    
                    with col_content:
                        st.markdown(f"""
                        <div style="background: #262730; border-radius: 8px; padding: 1rem; border: 1px solid #404040;">
                            <p style="margin: 0; color: #CCCCCC;"><strong style="color: #00FF88;">Source:</strong> {article['source']}</p>
                            <p style="margin: 0.5rem 0; color: #CCCCCC;"><strong style="color: #00FF88;">Published:</strong> {article['published']}</p>
                        """, unsafe_allow_html=True)
                        
                        if article['summary']:
                            summary_text = article['summary'][:300] + "..." if len(article['summary']) > 300 else article['summary']
                            st.markdown(f"<p style='margin: 0.5rem 0; color: #FAFAFA;'><strong style='color: #00FF88;'>Summary:</strong> {summary_text}</p>", unsafe_allow_html=True)
                        
                        if article['link']:
                            st.markdown(f"<a href='{article['link']}' target='_blank' style='color: #00FF88; text-decoration: none;'>🔗 Read Full Article</a>", unsafe_allow_html=True)
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    with col_sentiment:
                        sentiment_color = "#00FF88" if article['sentiment_score'] > 0 else "#FF4444" if article['sentiment_score'] < 0 else "#FFD700"
                        st.markdown(
                            f"""
                            <div class="metric-card" style="text-align: center; background: linear-gradient(135deg, {sentiment_color}20 0%, {sentiment_color}10 100%);">
                                <h4 style="color: {sentiment_color}; margin: 0;">{article['sentiment_label']}</h4>
                                <p style="margin: 0.5rem 0; color: #FAFAFA;">Score: {article['sentiment_score']:.3f}</p>
                                <p style="margin: 0; color: #CCCCCC;">Relevance: {article['relevance']:.2f}</p>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
        else:
            st.info("📰 No recent news articles available for this symbol. News sentiment analysis requires active news coverage.")
    else:
        # Show message when news sentiment is disabled
        if not data.get('news_data') and data.get('symbol'):
            st.markdown("""
            <div style="background: #262730; border-radius: 12px; padding: 1.5rem; margin: 1rem 0; border: 1px solid #404040;">
                <h3 style="color: #FFD700; margin: 0;">📰 News Sentiment Analysis</h3>
                <p style="margin: 0.5rem 0 0 0; color: #CCCCCC;">Enable "Show News Sentiment" in the sidebar to view real-time news analysis for market insights.</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Trading simulator actions
    if 'trading_mode' in locals() and trading_mode and trading_signal.get('signal') != 'UNKNOWN':
        col_buy, col_sell = st.columns(2)
        
        current_price = stock_info.get('currentPrice', 0)
        symbol = data['symbol']
        
        with col_buy:
            if st.button(f"🟢 BUY {symbol}", type="primary"):
                if investment_amount <= st.session_state.portfolio_balance:
                    shares = investment_amount / current_price
                    
                    if symbol in st.session_state.portfolio_holdings:
                        st.session_state.portfolio_holdings[symbol]['shares'] += shares
                        st.session_state.portfolio_holdings[symbol]['avg_price'] = (
                            (st.session_state.portfolio_holdings[symbol]['avg_price'] * 
                             (st.session_state.portfolio_holdings[symbol]['shares'] - shares) + 
                             current_price * shares) / st.session_state.portfolio_holdings[symbol]['shares']
                        )
                    else:
                        st.session_state.portfolio_holdings[symbol] = {
                            'shares': shares,
                            'avg_price': current_price
                        }
                    
                    st.session_state.portfolio_balance -= investment_amount
                    st.success(f"Bought {shares:.4f} shares of {symbol} at ${current_price:.2f}")
                    st.rerun()
                else:
                    st.error("Insufficient balance!")
        
        with col_sell:
            if symbol in st.session_state.portfolio_holdings and st.session_state.portfolio_holdings[symbol]['shares'] > 0:
                if st.button(f"🔴 SELL {symbol}", type="secondary"):
                    shares_to_sell = min(
                        investment_amount / current_price,
                        st.session_state.portfolio_holdings[symbol]['shares']
                    )
                    
                    proceeds = shares_to_sell * current_price
                    st.session_state.portfolio_balance += proceeds
                    st.session_state.portfolio_holdings[symbol]['shares'] -= shares_to_sell
                    
                    profit_loss = (current_price - st.session_state.portfolio_holdings[symbol]['avg_price']) * shares_to_sell
                    
                    if st.session_state.portfolio_holdings[symbol]['shares'] <= 0:
                        del st.session_state.portfolio_holdings[symbol]
                    
                    st.success(f"Sold {shares_to_sell:.4f} shares of {symbol} at ${current_price:.2f}")
                    if profit_loss > 0:
                        st.success(f"Profit: ${profit_loss:.2f}")
                    else:
                        st.error(f"Loss: ${abs(profit_loss):.2f}")
                    st.rerun()
    
    st.markdown("---")
    
    # Real-time update indicator
    last_updated = data.get('last_updated', datetime.now())
    st.info(f"🕐 Last Updated: {last_updated.strftime('%Y-%m-%d %H:%M:%S')} | Next update in real-time mode")
    
    # Header with basic info
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Current Price",
            value=f"${stock_info.get('currentPrice', 0):.2f}",
            delta=f"{stock_info.get('regularMarketChangePercent', 0):.2f}%"
        )
    
    with col2:
        st.metric(
            label="Market Cap",
            value=format_large_number(stock_info.get('marketCap', 0))
        )
    
    with col3:
        st.metric(
            label="P/E Ratio",
            value=f"{stock_info.get('trailingPE', 'N/A')}"
        )
    
    with col4:
        st.metric(
            label="52W High/Low",
            value=f"${stock_info.get('fiftyTwoWeekHigh', 0):.2f}",
            delta=f"Low: ${stock_info.get('fiftyTwoWeekLow', 0):.2f}"
        )
    
    # Charts section
    st.subheader(f"📊 {symbol} Price Chart")
    
    chart_generator = ChartGenerator()
    
    if chart_type == "Candlestick":
        fig = chart_generator.create_candlestick_chart(historical_data, symbol, trading_signal)
    elif chart_type == "Line":
        fig = chart_generator.create_line_chart(historical_data, symbol, trading_signal)
    elif chart_type == "OHLC":
        fig = chart_generator.create_ohlc_chart(historical_data, symbol)
    elif chart_type == "Bollinger Bands":
        fig = chart_generator.create_bollinger_bands_chart(historical_data, symbol)
    else:  # MACD Analysis
        fig = chart_generator.create_macd_chart(historical_data, symbol)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Data tables section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Historical Data")
        
        # Prepare data for display
        display_data = historical_data.copy()
        display_data = display_data.round(2)
        display_data.index = display_data.index.strftime('%Y-%m-%d')
        
        st.dataframe(
            display_data,
            use_container_width=True,
            height=400
        )
        
        # CSV download
        csv_buffer = io.StringIO()
        display_data.to_csv(csv_buffer)
        csv_data = csv_buffer.getvalue()
        
        st.download_button(
            label="📥 Download Historical Data (CSV)",
            data=csv_data,
            file_name=f"{symbol}_historical_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col2:
        st.subheader("💼 Company Information")
        
        # Company info table
        info_data = {
            "Company Name": stock_info.get('longName', 'N/A'),
            "Sector": stock_info.get('sector', 'N/A'),
            "Industry": stock_info.get('industry', 'N/A'),
            "Country": stock_info.get('country', 'N/A'),
            "Website": stock_info.get('website', 'N/A'),
            "Full Time Employees": format_large_number(stock_info.get('fullTimeEmployees', 0)),
            "Market Cap": format_large_number(stock_info.get('marketCap', 0)),
            "Enterprise Value": format_large_number(stock_info.get('enterpriseValue', 0)),
            "Revenue": format_large_number(stock_info.get('totalRevenue', 0)),
            "Profit Margin": f"{stock_info.get('profitMargins', 0)*100:.2f}%" if stock_info.get('profitMargins') else 'N/A',
            "Beta": f"{stock_info.get('beta', 'N/A')}",
            "Dividend Yield": f"{stock_info.get('dividendYield', 0)*100:.2f}%" if stock_info.get('dividendYield') else 'N/A'
        }
        
        info_df = pd.DataFrame(list(info_data.items()), columns=['Metric', 'Value'])
        st.dataframe(info_df, use_container_width=True, height=400)
        
        # Company info CSV download
        csv_buffer_info = io.StringIO()
        info_df.to_csv(csv_buffer_info, index=False)
        csv_info_data = csv_buffer_info.getvalue()
        
        st.download_button(
            label="📥 Download Company Info (CSV)",
            data=csv_info_data,
            file_name=f"{symbol}_company_info_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    # Technical indicators section
    st.subheader("📈 Technical Analysis")
    
    # Technical indicators chart (data already has indicators calculated)
    tech_fig = chart_generator.create_technical_chart(historical_data, symbol)
    st.plotly_chart(tech_fig, use_container_width=True)
    
    # Additional technical metrics
    col1, col2, col3, col4 = st.columns(4)
    
    latest_data = historical_data.iloc[-1]
    
    with col1:
        if 'MACD' in historical_data.columns:
            st.metric(
                label="MACD",
                value=f"{latest_data['MACD']:.3f}",
                delta=f"Signal: {latest_data['MACD_Signal']:.3f}",
                help="MACD above signal line = bullish momentum"
            )
    
    with col2:
        if 'BB_Upper' in historical_data.columns:
            bb_position = ((latest_data['Close'] - latest_data['BB_Lower']) / 
                          (latest_data['BB_Upper'] - latest_data['BB_Lower'])) * 100
            st.metric(
                label="Bollinger Band %",
                value=f"{bb_position:.1f}%",
                help="Position within Bollinger Bands (0-100%)"
            )
    
    with col3:
        if 'Volume_Ratio' in historical_data.columns:
            st.metric(
                label="Volume Ratio",
                value=f"{latest_data['Volume_Ratio']:.2f}",
                help="Current volume vs 20-day average"
            )
    
    with col4:
        if 'SMA_20' in historical_data.columns:
            price_vs_sma = ((latest_data['Close'] - latest_data['SMA_20']) / latest_data['SMA_20']) * 100
            st.metric(
                label="Price vs SMA20",
                value=f"{price_vs_sma:.2f}%",
                help="Price position relative to 20-day moving average"
            )
    
    # Portfolio Display Section
    if 'portfolio_holdings' in st.session_state and st.session_state.portfolio_holdings:
        st.subheader("📊 Portfolio Holdings")
        
        portfolio_data = []
        total_portfolio_value = st.session_state.portfolio_balance
        
        for symbol, holding in st.session_state.portfolio_holdings.items():
            if holding['shares'] > 0:
                # Get current price (simplified - using last known price)
                current_price = stock_info.get('currentPrice', holding['avg_price']) if data['symbol'] == symbol else holding['avg_price']
                current_value = holding['shares'] * current_price
                profit_loss = (current_price - holding['avg_price']) * holding['shares']
                profit_loss_pct = ((current_price - holding['avg_price']) / holding['avg_price']) * 100
                
                portfolio_data.append({
                    'Symbol': symbol,
                    'Shares': f"{holding['shares']:.4f}",
                    'Avg Price': f"${holding['avg_price']:.2f}",
                    'Current Price': f"${current_price:.2f}",
                    'Current Value': f"${current_value:.2f}",
                    'P&L': f"${profit_loss:.2f}",
                    'P&L %': f"{profit_loss_pct:.2f}%"
                })
                
                total_portfolio_value += current_value
        
        if portfolio_data:
            portfolio_df = pd.DataFrame(portfolio_data)
            st.dataframe(portfolio_df, use_container_width=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Cash Balance", f"${st.session_state.portfolio_balance:.2f}")
            with col2:
                st.metric("Total Portfolio Value", f"${total_portfolio_value:.2f}")
            with col3:
                total_return = total_portfolio_value - 1000.0  # Starting amount was $1000
                st.metric("Total Return", f"${total_return:.2f}", f"{(total_return/1000.0)*100:.2f}%")
    
    # Backtesting Results Section
    if data.get('backtest_results'):
        st.markdown("---")
        st.subheader("📊 Strategy Backtesting Results")
        
        backtest = data['backtest_results']
        
        # Performance overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            return_color = "green" if backtest['total_return_pct'] > 0 else "red"
            st.markdown(
                f"<div style='text-align: center; padding: 15px; background-color: {return_color}20; border-radius: 10px;'>"
                f"<h3 style='color: {return_color}; margin: 0;'>{backtest['total_return_pct']:.2f}%</h3>"
                f"<p style='margin: 0; color: #FAFAFA;'>Total Return</p>"
                f"</div>", 
                unsafe_allow_html=True
            )
        
        with col2:
            st.metric(
                "Annualized Return", 
                f"{backtest['annualized_return']:.2f}%",
                help="Expected yearly return based on historical performance"
            )
        
        with col3:
            st.metric(
                "Sharpe Ratio", 
                f"{backtest['sharpe_ratio']:.2f}",
                help="Risk-adjusted return (>1 is good, >2 is excellent)"
            )
        
        with col4:
            st.metric(
                "Max Drawdown", 
                f"{backtest['max_drawdown_pct']:.2f}%",
                help="Largest peak-to-trough decline"
            )
        
        # Trading statistics
        st.subheader("📈 Trading Performance")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Trades", backtest['total_trades'])
        
        with col2:
            win_rate_color = "green" if backtest['win_rate'] > 50 else "red"
            st.markdown(
                f"<div style='text-align: center; padding: 10px; background-color: {win_rate_color}20; border-radius: 5px;'>"
                f"<strong style='color: {win_rate_color};'>{backtest['win_rate']:.1f}%</strong><br>"
                f"<small>Win Rate</small>"
                f"</div>", 
                unsafe_allow_html=True
            )
        
        with col3:
            st.metric("Avg Win", f"${backtest['avg_win']:.2f}")
        
        with col4:
            st.metric("Avg Loss", f"${backtest['avg_loss']:.2f}")
        
        # Performance chart
        if backtest['daily_values'] and len(backtest['daily_values']) > 0:
            st.subheader("📊 Portfolio Value Over Time")
            
            portfolio_df = pd.DataFrame({
                'Date': pd.to_datetime(backtest['dates']) if backtest['dates'] else [],
                'Portfolio Value': backtest['daily_values']
            })
            
            if not portfolio_df.empty:
                import plotly.graph_objects as go
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=portfolio_df['Date'],
                    y=portfolio_df['Portfolio Value'],
                    mode='lines',
                    name='Portfolio Value',
                    line=dict(color='#00FF88', width=2)
                ))
                
                # Add buy/sell signals to the chart
                if backtest['buy_signals']:
                    buy_dates = [signal['date'] for signal in backtest['buy_signals']]
                    buy_values = [signal['price'] * (backtest['initial_capital'] / backtest['buy_signals'][0]['price']) for signal in backtest['buy_signals']]
                    
                    fig.add_trace(go.Scatter(
                        x=buy_dates,
                        y=buy_values,
                        mode='markers',
                        name='Buy Signals',
                        marker=dict(color='green', size=10, symbol='triangle-up')
                    ))
                
                if backtest['sell_signals']:
                    sell_dates = [signal['date'] for signal in backtest['sell_signals']]
                    sell_values = [signal['price'] * (backtest['initial_capital'] / backtest['sell_signals'][0]['price']) for signal in backtest['sell_signals']]
                    
                    fig.add_trace(go.Scatter(
                        x=sell_dates,
                        y=sell_values,
                        mode='markers',
                        name='Sell Signals',
                        marker=dict(color='red', size=10, symbol='triangle-down')
                    ))
                
                fig.update_layout(
                    title="Backtesting Results: Portfolio Performance",
                    xaxis_title="Date",
                    yaxis_title="Portfolio Value ($)",
                    plot_bgcolor='#0E1117',
                    paper_bgcolor='#262730',
                    font=dict(color='#FAFAFA'),
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        # Strategy assessment
        st.subheader("🎯 Strategy Assessment")
        
        # Calculate strategy rating
        score = 0
        if backtest['total_return_pct'] > 10: score += 2
        elif backtest['total_return_pct'] > 0: score += 1
        
        if backtest['sharpe_ratio'] > 1.5: score += 2
        elif backtest['sharpe_ratio'] > 1: score += 1
        
        if backtest['win_rate'] > 60: score += 2
        elif backtest['win_rate'] > 50: score += 1
        
        if backtest['max_drawdown_pct'] < 10: score += 2
        elif backtest['max_drawdown_pct'] < 20: score += 1
        
        if score >= 7:
            rating = "🟢 Excellent Strategy"
            rating_color = "green"
            recommendation = "Strong buy signal strategy with good risk management"
        elif score >= 5:
            rating = "🟡 Good Strategy"
            rating_color = "orange"
            recommendation = "Decent strategy but monitor risk levels"
        elif score >= 3:
            rating = "🟠 Average Strategy"
            rating_color = "orange"
            recommendation = "Strategy shows potential but needs improvement"
        else:
            rating = "🔴 Poor Strategy"
            rating_color = "red"
            recommendation = "Strategy underperforms - consider adjustments"
        
        st.markdown(
            f"<div style='padding: 20px; background-color: {rating_color}20; border-left: 5px solid {rating_color}; border-radius: 10px;'>"
            f"<h3 style='color: {rating_color}; margin: 0;'>{rating}</h3>"
            f"<p style='margin: 10px 0 0 0; color: #FAFAFA;'>{recommendation}</p>"
            f"<small style='color: #CCCCCC;'>Strategy Score: {score}/8</small>"
            f"</div>", 
            unsafe_allow_html=True
        )

def format_large_number(num):
    """Format large numbers with appropriate suffixes"""
    if not num or num == 0:
        return "N/A"
    
    num = float(num)
    if num >= 1e12:
        return f"${num/1e12:.2f}T"
    elif num >= 1e9:
        return f"${num/1e9:.2f}B"
    elif num >= 1e6:
        return f"${num/1e6:.2f}M"
    elif num >= 1e3:
        return f"${num/1e3:.2f}K"
    else:
        return f"${num:.2f}"

if __name__ == "__main__":
    main()
