import sys
import warnings
import os
from datetime import datetime
from crew.crew import StockAnalysisCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the stock analysis crew.
    """
    # Get stock symbol from command line or use "AAPL"
    symbol = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    
    inputs = {
        'symbol': symbol.upper(),
        'period': '5y'  # 5 years of data
    }

    try:
        result = StockAnalysisCrew().crew().kickoff(inputs=inputs)

        print("\n" + "=" * 50)
        print("✅ Stock Analysis Complete!")
        print(f"Generated files:")
        print(f"   - {symbol.upper()}_stock_data.csv")
        print(f"   - {symbol.upper()}_analysis.json") 
        print(f"   - {symbol.upper()}_analysis_chart.html")
        print(f"   - {symbol.upper()}_analysis_report.md")
        print(f"   - report.md")
        
        return result
        
    except Exception as e:
        print(f"❌ An error occurred while running the crew: {e}")
        raise Exception(f"An error occurred while running the crew: {e}")

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        StockAnalysisCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        StockAnalysisCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    
    try:
        StockAnalysisCrew().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")