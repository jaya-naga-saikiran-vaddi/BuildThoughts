from langchain.agents import Tool, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from dotenv import load_dotenv

from mcp_server.tools.mysql_tool import fetch_mysql_data
from mcp_server.tools.postgres_tool import fetch_postgres_data
from mcp_server.tools.compare_tool import compare_tables
from mcp_server.tools.report_tool import generate_report
from mcp_server.utils.logger import log_trace

load_dotenv()


def run_comparison_job(goal, table_name):
    tools = [
        Tool(name="FetchMySQL", func=lambda _: fetch_mysql_data(table_name), description="Fetch data from MySQL"),
        Tool(name="FetchPostgres", func=lambda _: fetch_postgres_data(table_name),
             description="Fetch data from Postgres"),
        Tool(name="CompareTables", func=compare_tables, description="Compare two sets of data"),
        Tool(name="GenerateReport", func=generate_report, description="Generate a difference report"),
    ]

    agent = initialize_agent(tools, ChatOpenAI(temperature=0), agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                             verbose=True)
    result = agent.run(goal)
    log_trace(goal, result)
    return result
