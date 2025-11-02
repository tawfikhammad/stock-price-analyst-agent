from pydantic import BaseModel, Field

class StockDataInput(BaseModel):
    symbol: str = Field(..., description="Stock symbol (e.g., google")
    period: str = Field(default="1m", description="Period for data")

class StockAnalysisInput(BaseModel):
    symbol: str = Field(..., description="Stock symbol for analysis")
    data_path: str = Field(default="", description="Optional: Path to saved stock data CSV file")

class ReportGeneratorInput(BaseModel):
    symbol: str = Field(..., description="Stock symbol")
