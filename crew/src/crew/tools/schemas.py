from typing import Type, Dict, Any
from pydantic import BaseModel, Field

class StockDataInput(BaseModel):
    """Input schema for Stock Data Fetcher."""
    symbol: str = Field(..., description="Stock symbol (e.g., google")
    period: str = Field(default="1m", description="Period for data")

class StockAnalysisInput(BaseModel):
    """Input schema for Stock Analysis."""
    symbol: str = Field(..., description="Stock symbol for analysis")
    data_path: str = Field(default="", description="Optional: Path to saved stock data CSV file")

class ReportGeneratorInput(BaseModel):
    """Input schema for Report Generator."""
    symbol: str = Field(..., description="Stock symbol")
