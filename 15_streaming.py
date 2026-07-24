from langchain.tools import tool
from langgraph.config import get_stream_writer
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

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
for chunk in agent.stream(
    {"messages": [HumanMessage("济南的天气如何")]},
    stream_mode=["updates","messages","custom"],
    version="v2",
):
    print(chunk)
    # if chunk["type"] == "messages":
    #     token, metadata = chunk["data"]
    #     print(f"node: {metadata['langgraph_node']}")
    #     print(f"content: {token.content_blocks}")
    #     print("\n")