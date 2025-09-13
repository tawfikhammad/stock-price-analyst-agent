# Stock Price Visualizer Agent

An AI-powered stock analysis system built with CrewAI that provides comprehensive technical analysis, market sentiment research, and investment recommendations for stocks.

## Features

- **Technical Analysis**: Advanced stock data analysis with technical indicators (RSI, MACD, Bollinger Bands, Moving Averages)
- **Market Sentiment Analysis**: Research and analyze recent financial news and market sentiment
- **Investment Reports**: Generate professional executive investment briefs with buy/sell/hold recommendations
- **Data Visualization**: Create interactive charts and visualizations using Plotly and Matplotlib

## System Architecture

The system consists of 3 AI agents:

1. **Stock Data Analyst**: Fetches and analyzes stock price data with technical indicators
2. **News Research Specialist**: Researches financial news and analyzes market sentiment  
3. **Investment Advisor**: Synthesizes analysis into professional investment recommendations

## Project Structure

```
crew/
├── .env                         # Environment variables
├── pyproject.toml              # Project configuration
├── uv.lock                     # Dependency lock file
├── artifacts/                  # Generated analysis outputs
├── src/crew/
│   ├── crew.py                 # Main crew definition
│   ├── main.py                 # Entry point
│   ├── config/
│   │   ├── agents.yaml         # Agent configurations
│   │   └── tasks.yaml          # Task definitions
│   └── tools/
│       ├── custom_tools.py     # Stock analysis tools
│       ├── helper.py           # Utility functions
│       └── schemas.py          # Data schemas
└── tests/                      # Test files
```


## Installation

1. Clone the repository:
```bash
git clone https://github.com/tawfikhammad/stock-price-analyst-agent.git
cd stock-price-visualizer-agent/crew
```

2. Install dependencies using uv (recommended):
```bash
uv sync
```

3. Set up environment variables:
Create a `.env` file in the crew directory and add your API keys:
```
SERPER_API_KEY=your_serper_api_key_here
```

## Usage

```bash
cd crew

crewai run
```

When prompted, enter:
- **Stock symbol** (e.g., AAPL, GOOGL, MSFT)
- **Analysis period** (e.g., 1m, 3m, 6m, 1y, 2y, 5y, max)

### Generated Outputs

The system generates several output files in the `artifacts/` directory:

- `{SYMBOL}_stock_data.csv` - Raw historical stock data
- `{SYMBOL}_analysis.json` - Detailed technical analysis results
- `{SYMBOL}_analysis_chart.html` - Interactive stock price chart
- `{SYMBOL}_analysis_report.md` - Technical analysis report
- `report.md` - Executive investment brief

  ![analysis_chart](https://github.com/tawfikhammad/stock-price-analyst-agent/blob/492a7006dc16c3b0c6ec4226de22ea644dade178/crew/artifacts/image.png)
