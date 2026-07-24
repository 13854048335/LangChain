from pprint import pprint
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage


@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"


agent = create_agent(model="deepseek-v4-pro", tools=[search])
response = agent.invoke(
    {"messages": HumanMessage(content="帮我查询杭州的天气")}
)
pprint(response)