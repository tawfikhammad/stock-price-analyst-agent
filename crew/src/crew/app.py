import streamlit as st
import os
import json
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import warnings
from crew.crew import StockAnalysisCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Page configuration
st.set_page_config(
    page_title="Stock Price Visualizer & Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    .stAlert {
        padding: 10px;
        border-radius: 5px;
    }
    h1 {
        color: #1f77b4;
    }
    h2 {
        color: #2c3e50;
    }
    </style>
""", unsafe_allow_html=True)

def load_analysis_data(symbol):
    """Load analysis data from JSON file"""
    analysis_file = f"artifacts/{symbol}_analysis.json"
    if os.path.exists(analysis_file):
        with open(analysis_file, 'r') as f:
            return json.load(f)
    return None

def load_stock_data(symbol):
    """Load stock data from CSV file"""
    data_file = f"artifacts/{symbol}_stock_data.csv"
    if os.path.exists(data_file):
        df = pd.read_csv(data_file, index_col=0, parse_dates=True)
        return df
    return None

def load_report(symbol):
    """Load markdown report"""
    report_file = f"artifacts/{symbol}_analysis_report.md"
    if os.path.exists(report_file):
        with open(report_file, 'r') as f:
            return f.read()
    
    # Fallback to main report
    main_report = "artifacts/report.md"
    if os.path.exists(main_report):
        with open(main_report, 'r') as f:
            return f.read()
    return None

def create_price_chart(df, symbol):
    """Create interactive price chart with indicators"""
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.5, 0.25, 0.25],
        subplot_titles=(f'{symbol} Stock Price & Moving Averages', 'RSI', 'MACD')
    )
    
    # Price and Moving Averages
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='Price'
    ), row=1, col=1)
    
    if 'MA_20' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['MA_20'], 
                                name='MA 20', line=dict(color='orange', width=1)), row=1, col=1)
    if 'MA_50' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['MA_50'], 
                                name='MA 50', line=dict(color='blue', width=1)), row=1, col=1)
    if 'MA_200' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['MA_200'], 
                                name='MA 200', line=dict(color='red', width=1)), row=1, col=1)
    
    # Bollinger Bands
    if 'BB_upper' in df.columns and 'BB_lower' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['BB_upper'], 
                                name='BB Upper', line=dict(color='gray', width=1, dash='dash')), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['BB_lower'], 
                                name='BB Lower', line=dict(color='gray', width=1, dash='dash'), 
                                fill='tonexty', fillcolor='rgba(128,128,128,0.1)'), row=1, col=1)
    
    # RSI
    if 'RSI' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], 
                                name='RSI', line=dict(color='purple', width=2)), row=2, col=1)
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
    
    # MACD
    if 'MACD' in df.columns and 'MACD_signal' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], 
                                name='MACD', line=dict(color='blue', width=2)), row=3, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['MACD_signal'], 
                                name='Signal', line=dict(color='red', width=2)), row=3, col=1)
        fig.add_hline(y=0, line_dash="dash", line_color="gray", row=3, col=1)
    
    fig.update_layout(
        height=900,
        showlegend=True,
        xaxis_rangeslider_visible=False,
        hovermode='x unified'
    )
    
    fig.update_xaxes(title_text="Date", row=3, col=1)
    fig.update_yaxes(title_text="Price ($)", row=1, col=1)
    fig.update_yaxes(title_text="RSI", row=2, col=1)
    fig.update_yaxes(title_text="MACD", row=3, col=1)
    
    return fig

def create_volume_chart(df, symbol):
    """Create volume chart"""
    fig = go.Figure()
    
    colors = ['red' if df['Close'][i] < df['Open'][i] else 'green' 
              for i in range(len(df))]
    
    fig.add_trace(go.Bar(
        x=df.index,
        y=df['Volume'],
        name='Volume',
        marker_color=colors
    ))
    
    fig.update_layout(
        title=f'{symbol} Trading Volume',
        xaxis_title='Date',
        yaxis_title='Volume',
        height=400,
        hovermode='x unified'
    )
    
    return fig

def display_metrics(analysis_data):
    """Display key metrics in columns"""
    col1, col2, col3, col4 = st.columns(4)
    
    price_stats = analysis_data.get('price_stats', {})
    tech_indicators = analysis_data.get('technical_indicators', {})
    
    with col1:
        st.metric(
            label="Current Price",
            value=f"${price_stats.get('current_price', 'N/A')}",
            delta=None
        )
        st.metric(
            label="Average Price",
            value=f"${price_stats.get('average_price', 'N/A')}"
        )
    
    with col2:
        st.metric(
            label="Highest Price",
            value=f"${price_stats.get('highest_price', 'N/A')}"
        )
        st.metric(
            label="Lowest Price",
            value=f"${price_stats.get('lowest_price', 'N/A')}"
        )
    
    with col3:
        st.metric(
            label="RSI",
            value=f"{tech_indicators.get('rsi', 'N/A')}"
        )
        st.metric(
            label="MA 50",
            value=f"${tech_indicators.get('ma_50', 'N/A')}"
        )
    
    with col4:
        st.metric(
            label="MACD",
            value=f"{tech_indicators.get('macd', 'N/A')}"
        )
        st.metric(
            label="MA 200",
            value=f"${tech_indicators.get('ma_200', 'N/A')}"
        )

def display_analysis_summary(analysis_data):
    """Display analysis summary"""
    trend = analysis_data.get('trend_analysis', {})
    volatility = analysis_data.get('volatility_analysis', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Trend Analysis")
        
        trend_direction = trend.get('trend_direction', 'N/A')
        trend_color = "🟢" if trend_direction == "Bullish" else "🔴"
        st.markdown(f"**Trend Direction:** {trend_color} {trend_direction}")
        
        st.markdown(f"**Price vs MA20:** {trend.get('price_vs_ma20', 'N/A')}")
        st.markdown(f"**Price vs MA50:** {trend.get('price_vs_ma50', 'N/A')}")
        st.markdown(f"**Price vs MA200:** {trend.get('price_vs_ma200', 'N/A')}")
        
        rsi_signal = trend.get('rsi_signal', 'N/A')
        if rsi_signal == "Overbought":
            st.markdown(f"**RSI Signal:** 🔴 {rsi_signal}")
        elif rsi_signal == "Oversold":
            st.markdown(f"**RSI Signal:** 🟢 {rsi_signal}")
        else:
            st.markdown(f"**RSI Signal:** ⚪ {rsi_signal}")
    
    with col2:
        st.subheader("📉 Volatility Analysis")
        st.markdown(f"**Daily Volatility:** {volatility.get('daily_volatility', 'N/A')}")
        st.markdown(f"**Annualized Volatility:** {volatility.get('annualized_volatility', 'N/A')}")
        st.markdown(f"**Max Daily Gain:** {volatility.get('max_daily_gain', 'N/A')}")
        st.markdown(f"**Max Daily Loss:** {volatility.get('max_daily_loss', 'N/A')}")

def main():
    st.title("📈 Stock Price Visualizer & Analysis")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Stock symbol input
        symbol = st.text_input(
            "Stock Symbol",
            value="AAPL",
            help="Enter stock ticker symbol (e.g., AAPL, MSFT, GOOGL)"
        ).upper()
        
        # Period selection
        period = st.selectbox(
            "Analysis Period",
            options=["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "max"],
            index=4,
            help="Select the time period for analysis"
        )
        
        # Analyze button
        analyze_button = st.button("🔍 Analyze Stock", type="primary", use_container_width=True)
        
        st.markdown("---")
        st.info("💡 **Tip:** Enter a stock symbol and click 'Analyze Stock' to generate comprehensive analysis with AI-powered insights.")
        
        st.markdown("---")
        st.caption("Built with Streamlit & CrewAI")
    
    # Main content
    if analyze_button:
        if not symbol:
            st.error("⚠️ Please enter a stock symbol")
            return
        
        with st.spinner(f"🔄 Analyzing {symbol}... This may take a few minutes..."):
            try:
                # Run the crew analysis
                inputs = {
                    'symbol': symbol,
                    'period': period
                }
                
                result = StockAnalysisCrew().crew().kickoff(inputs=inputs)
                
                st.success(f"✅ Analysis complete for {symbol}!")
                
                # Force a rerun to display results
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error analyzing {symbol}: {str(e)}")
                st.exception(e)
    
    # Display results if available
    analysis_data = load_analysis_data(symbol)
    stock_data = load_stock_data(symbol)
    report = load_report(symbol)
    
    if analysis_data and stock_data is not None:
        # Display metrics
        st.header(f"📊 {symbol} Analysis Dashboard")
        display_metrics(analysis_data)
        
        st.markdown("---")
        
        # Display charts
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Price Chart", "📊 Volume", "📋 Summary", "📄 Full Report"])
        
        with tab1:
            st.plotly_chart(create_price_chart(stock_data, symbol), use_container_width=True)
        
        with tab2:
            st.plotly_chart(create_volume_chart(stock_data, symbol), use_container_width=True)
        
        with tab3:
            display_analysis_summary(analysis_data)
            
            # Display technical indicators table
            st.subheader("🔧 Technical Indicators")
            tech_df = pd.DataFrame([analysis_data.get('technical_indicators', {})])
            st.dataframe(tech_df, use_container_width=True)
        
        with tab4:
            if report:
                st.markdown(report)
            else:
                st.warning("⚠️ Report not available. Please run the analysis first.")
        
        # Download options
        st.markdown("---")
        st.subheader("⬇️ Download Data")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if os.path.exists(f"artifacts/{symbol}_stock_data.csv"):
                with open(f"artifacts/{symbol}_stock_data.csv", 'r') as f:
                    st.download_button(
                        label="📥 Download CSV Data",
                        data=f.read(),
                        file_name=f"{symbol}_stock_data.csv",
                        mime="text/csv"
                    )
        
        with col2:
            if os.path.exists(f"artifacts/{symbol}_analysis.json"):
                with open(f"artifacts/{symbol}_analysis.json", 'r') as f:
                    st.download_button(
                        label="📥 Download Analysis JSON",
                        data=f.read(),
                        file_name=f"{symbol}_analysis.json",
                        mime="application/json"
                    )
        
        with col3:
            if report:
                st.download_button(
                    label="📥 Download Report",
                    data=report,
                    file_name=f"{symbol}_report.md",
                    mime="text/markdown"
                )
    
    else:
        # Welcome screen
        st.info("""
        👋 **Welcome to Stock Price Visualizer & Analysis!**
        
        This application uses AI-powered agents to provide comprehensive stock analysis including:
        - 📊 Technical analysis with multiple indicators (RSI, MACD, Bollinger Bands)
        - 📈 Interactive price charts and visualizations
        - 📰 News sentiment analysis
        - 💼 Investment recommendations
        - 📄 Detailed analysis reports
        
        **Get started:**
        1. Enter a stock symbol in the sidebar (e.g., AAPL, MSFT, GOOGL)
        2. Select your preferred analysis period
        3. Click "🔍 Analyze Stock"
        4. Explore the comprehensive analysis dashboard
        
        The analysis is performed by AI agents specialized in:
        - Stock data analysis
        - Financial news research
        - Investment advisory
        """)
        
        # Display sample if AAPL data exists
        if os.path.exists("artifacts/AAPL_analysis.json"):
            st.markdown("---")
            st.subheader("📌 Sample Analysis Available")
            st.info("Sample AAPL analysis is available. View the results above or analyze a different stock.")

if __name__ == "__main__":
    main()
