from datetime import datetime     

def generate_report(analysis_data: dict) -> str:
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
