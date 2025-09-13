from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel
import yfinance as yf
import pandas as pd
import numpy as np
from .helper import create_stock_charts, generate_report 
from .schemas import (
    StockDataInput,
    StockAnalysisInput,
    ReportGeneratorInput
)
import json, os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class StockDataFetcher(BaseTool):
    name: str = "Stock Data Fetcher"
    description: str = "".join(
        [
            "Fetches historical stock price data using yfinance. ",
            "Returns data and saves it to CSV file for analysis."
        ]
    )
    args_schema: Type[BaseModel] = StockDataInput

    def _run(self, symbol: str, period: str = "1m") -> str:
        try:
            os.makedirs("artifacts", exist_ok=True)
            
            # Fetch stock data
            stock = yf.Ticker(symbol)
            data = stock.history(period=period)
            
            if data.empty:
                return f"No data found for symbol {symbol}"
            
            # Save historical data to CSV
            filename = f"artifacts/{symbol}_stock_data.csv"
            data.to_csv(filename)
            
            # Calculate basic metrics السعر اللي قفل عليه السهم
            current_price = data['Close'][-1]
            price_change = data['Close'][-1] - data['Close'][-2]

            # Volume analysis عدد الاسهم اللي اتباعت
            avg_volume = data['Volume'].mean()
            latest_volume = data['Volume'][-1]

            result = {
                "symbol": symbol,
                "current_price": round(current_price, 2),
                "price_change": round(price_change, 2),
                "period": period,
                "date_range": f"{data.index[0].strftime('%Y-%m-%d')} to {data.index[-1].strftime('%Y-%m-%d')}",
                "avg_volume": int(avg_volume),
                "latest_volume": int(latest_volume),
            }
            
            return f"Successfully fetched data for {symbol}:\n" + json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Error fetching data for {symbol}: {str(e)}"

class StockAnalyzer(BaseTool):
    name: str = "Stock Price Analyzer"
    description: str = "".join(
        [
            "Performs statistical analysis on stock data including technical indicators, ",
            "volatility analysis, trend analysis, and generates visualizations."
        ]
    )
    args_schema: Type[BaseModel] = StockAnalysisInput

    def _run(self, symbol: str, data_path: str = "") -> str:
        try:
            # Load data
            if data_path and os.path.exists(data_path):
                df = pd.read_csv(data_path, index_col=0, parse_dates=True)
            else:
                filename = f"artifacts/{symbol}_stock_data.csv"
                if not os.path.exists(filename):
                    return f"No data file found for {symbol}. Please fetch data first."
                df = pd.read_csv(filename, index_col=0, parse_dates=True)
            
            # Moving averages
            df['MA_20'] = df['Close'].rolling(window=20).mean()
            df['MA_50'] = df['Close'].rolling(window=50).mean()
            df['MA_200'] = df['Close'].rolling(window=200).mean()
            
            # Bollinger Bands
            df['BB_upper'] = df['MA_20'] + (df['Close'].rolling(window=20).std() * 2)
            df['BB_lower'] = df['MA_20'] - (df['Close'].rolling(window=20).std() * 2)
            
            # Relative Strength Index calculation
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
            
            # MACD
            exp1 = df['Close'].ewm(span=12).mean()
            exp2 = df['Close'].ewm(span=26).mean()
            df['MACD'] = exp1 - exp2
            df['MACD_signal'] = df['MACD'].ewm(span=9).mean()
            
            # Statistical Analysis
            returns = df['Close'].pct_change().dropna()
            
            analysis_results = {
                "symbol": symbol,
                "analysis_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "price_stats": {
                    "current_price": round(df['Close'][-1], 2),
                    "highest_price": round(df['High'].max(), 2),
                    "lowest_price": round(df['Low'].min(), 2),
                    "average_price": round(df['Close'].mean(), 2),
                },
                "technical_indicators": {
                    "ma_20": round(df['MA_20'][-1], 2),
                    "ma_50": round(df['MA_50'][-1], 2),
                    "ma_200": round(df['MA_200'][-1], 2),
                    "rsi": round(df['RSI'][-1], 2),
                    "macd": round(df['MACD'][-1], 4),
                    "macd_signal": round(df['MACD_signal'][-1], 4),
                    "bollinger_upper": round(df['BB_upper'][-1], 2),
                    "bollinger_lower": round(df['BB_lower'][-1], 2)
                },
                "volatility_analysis": {
                    "daily_volatility": round(returns.std(), 4),
                    "annualized_volatility": round(returns.std() * np.sqrt(252), 4),
                    "max_daily_gain": round(returns.max(), 4),
                    "max_daily_loss": round(returns.min(), 4)
                },
                "trend_analysis": {
                    "trend_direction": "Bullish" if df['Close'][-1] > df['MA_50'][-1] else "Bearish",
                    "price_vs_ma20": "Above" if df['Close'][-1] > df['MA_20'][-1] else "Below",
                    "price_vs_ma50": "Above" if df['Close'][-1] > df['MA_50'][-1] else "Below",
                    "price_vs_ma200": "Above" if df['Close'][-1] > df['MA_200'][-1] else "Below",
                    "rsi_signal": "Overbought" if df['RSI'][-1] > 70 else "Oversold" if df['RSI'][-1] < 30 else "Neutral"
                }
            }
            
            # Create visualizations
            create_stock_charts(df, symbol)

            # Save analysis results
            analysis_file = f"artifacts/{symbol}_analysis.json"
            with open(analysis_file, 'w') as f:
                json.dump(analysis_results, f, indent=2)
            
            return f"Stock analysis completed for {symbol}:\n" + json.dumps(analysis_results, indent=2)
            
        except Exception as e:
            return f"Error analyzing stock data for {symbol}: {str(e)}"
        
class ReportGenerator(BaseTool):
    name: str = "Report Generator"
    description: str = (
        "Generates a report combining stock analysis, news sentiment, and investment recommendations in a professional format."
    )
    args_schema: Type[BaseModel] = ReportGeneratorInput

    def _run(self, symbol: str) -> str:
        try:
            analysis_file = f"artifacts/{symbol}_analysis.json"
            if not os.path.exists(analysis_file):
                return f"No analysis file found for {symbol}. Please run the analysis first."
                 
            # Load analysis data
            with open(analysis_file, 'r') as f:
                analysis_data = json.load(f)
            
            # Generate summary
            report = generate_report(analysis_data)
            
            # Save report
            report_file = f"artifacts/{symbol}_analysis_report.md"
            with open(report_file, 'w') as f:
                f.write(report)
            
            return f"""Executive report generated successfully and saved as {report_file}\n\n
            Report Preview:\n{report}..."""
            
        except Exception as e:
            return f"Error generating executive report: {str(e)}"