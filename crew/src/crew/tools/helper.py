import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime

def create_stock_charts(df: pd.DataFrame, symbol: str):
        # Create subplots
        fig = make_subplots(
            rows=4, cols=1,
            subplot_titles=(f'{symbol} Stock Price & Moving Averages', 
                          'Volume', 'RSI', 'MACD'),
            vertical_spacing=0.05,
            row_heights=[0.4, 0.2, 0.2, 0.2]
        )
        
        # Price and Moving Averages
        fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Close Price', line=dict(color='blue')), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['MA_20'], name='MA 20', line=dict(color='red')), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['MA_50'], name='MA 50', line=dict(color='green')), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['MA_200'], name='MA 200', line=dict(color='purple')), row=1, col=1)
        
        # Bollinger Bands
        fig.add_trace(go.Scatter(x=df.index, y=df['BB_upper'], name='BB Upper', line=dict(color='gray', dash='dash')), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['BB_lower'], name='BB Lower', line=dict(color='gray', dash='dash')), row=1, col=1)
        
        # Volume
        fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume', marker_color='lightblue'), row=2, col=1)
        
        # RSI
        fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI', line=dict(color='orange')), row=3, col=1)
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)
        
        # MACD
        fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], name='MACD', line=dict(color='blue')), row=4, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['MACD_signal'], name='Signal', line=dict(color='red')), row=4, col=1)
        
        # Update layout
        fig.update_layout(
            title=f'{symbol} Stock Analysis Dashboard',
            height=1000,
            showlegend=True,
            xaxis_rangeslider_visible=False
        )
        
        # Save chart
        chart_file = f"artifacts/{symbol}_analysis_chart.html"
        fig.write_html(chart_file)
        
        print(f"Chart saved as {chart_file}")


def generate_executive_report(analysis_data: dict) -> str:
    """Generate comprehensive executive report"""
    symbol = analysis_data['symbol']
    
    # Determine investment recommendation
    tech_indicators = analysis_data['technical_indicators']
    trend = analysis_data['trend_analysis']
    volatility = analysis_data['volatility_analysis']

    report = f"""# Executive Investment Brief: {symbol}
## Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Key Financial Metrics

| Metric | Value |
|--------|-------|
| Current Price | ${analysis_data['price_stats']['current_price']} |
| 52-Week High | ${analysis_data['price_stats']['highest_price']} |
| 52-Week Low | ${analysis_data['price_stats']['lowest_price']} |
| Average Price | ${analysis_data['price_stats']['average_price']} |
| Daily Volatility | {volatility['daily_volatility']:.2%} |
| Annualized Volatility | {volatility['annualized_volatility']:.2%} |

## Technical Analysis Summary

### Moving Averages
- **20-Day MA:** ${tech_indicators['ma_20']} ({trend['price_vs_ma20']} current price)
- **50-Day MA:** ${tech_indicators['ma_50']} ({trend['price_vs_ma50']} current price)  
- **200-Day MA:** ${tech_indicators['ma_200']} ({trend['price_vs_ma200']} current price)

### Technical Indicators
- **RSI (14):** {tech_indicators['rsi']} - {trend['rsi_signal']}
- **MACD:** {tech_indicators['macd']:.4f}
- **MACD Signal:** {tech_indicators['macd_signal']:.4f}
- **Trend Direction:** {trend['trend_direction']}

### Bollinger Bands
- **Upper Band:** ${tech_indicators['bollinger_upper']}
- **Lower Band:** ${tech_indicators['bollinger_lower']}

### Strengths:
"""
    # Add strengths based on analysis
    strengths = []
    if trend['trend_direction'] == 'Bullish':
        strengths.append("Stock is in a bullish trend above key moving averages")
    if volatility['annualized_volatility'] < 0.2:
        strengths.append("Low volatility indicates stable price movements")
    if tech_indicators['rsi'] < 70 and tech_indicators['rsi'] > 30:
        strengths.append("RSI indicates stock is neither overbought nor oversold")
    
    for strength in strengths:
        report += f"- {strength}\n"
    
    report += f"\n### Risks:\n"
        
    # Add risks based on analysis
    risks = []
    if volatility['annualized_volatility'] > 0.4:
        risks.append("High volatility may indicate increased investment risk")
    if trend['trend_direction'] == 'Bearish':
        risks.append("Stock is currently in a bearish trend")
    if tech_indicators['rsi'] > 70:
        risks.append("RSI indicates stock may be overbought")
    elif tech_indicators['rsi'] < 30:
        risks.append("RSI indicates stock may be oversold")
    
    for risk in risks:
        report += f"- {risk}\n"
    
    report += f"""

## Performance Metrics

### Risk Assessment:
- **Maximum Daily Gain:** {volatility['max_daily_gain']:.2%}
- **Maximum Daily Loss:** {volatility['max_daily_loss']:.2%}
- **Risk Level:** {"High" if volatility['annualized_volatility'] > 0.4 else "Medium" if volatility['annualized_volatility'] > 0.2 else "Low"}

### Price Targets:
- **Resistance Level:** ${tech_indicators['bollinger_upper']}
- **Support Level:** ${tech_indicators['bollinger_lower']}
- **Fair Value Estimate:** ${analysis_data['price_stats']['average_price']}
"""
        
    return report
