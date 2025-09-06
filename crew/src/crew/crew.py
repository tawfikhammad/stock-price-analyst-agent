from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool
from typing import List
from crew.tools.custom_tools import (
    StockDataFetcher, 
    StockAnalyzer, 
    ReportGenerator
)

@CrewBase
class StockAnalysisCrew():
    """Stock Price Visualizer and Analysis Crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def stock_data_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['stock_data_analyst'],
            tools=[StockDataFetcher(), StockAnalyzer()],
            verbose=True,
            memory=True,
        )
    
    @agent
    def news_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['news_researcher'],
            tools=[SerperDevTool()],
            verbose=True,
            memory=True,
        )

    @agent
    def investment_report(self) -> Agent:
        return Agent(
            config=self.agents_config['investment_report'],
            tools=[ReportGenerator()],
            verbose=True,
            memory=True,
        )

    @task
    def stock_data_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['stock_data_analysis_task'],
        )

    @task
    def news_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['news_research_task'],
        )

    @task
    def investment_report_task(self) -> Task:
        return Task(
            config=self.tasks_config['investment_report_task'],
            markdown=True,
            output_file='artifacts/report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Stock Analysis crew"""
       
        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )
