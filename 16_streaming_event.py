from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain.tools import tool
from langgraph.config import get_stream_writer

@tool
def get_weather(city: str) -> str:
    """获取某个城市的天气."""
    writer = get_stream_writer()
    # stream any arbitrary data
    writer(f"查找城市数据: {city}")
    writer(f"城市获取数据: {city}")
    return f"这里总是阳光明媚 {city}!"


agent = create_agent(
    model="deepseek-v4-pro",
    tools=[get_weather],
)


stream = agent.stream_events(
    {"messages": [HumanMessage("北京天气怎么样?")]},
    version="v3",
)
for message in stream.messages:
    for token in message.reasoning:
        print(f"[思考] {token}", end="")
    for token in message.text:
        print(token, end="", flush=True)