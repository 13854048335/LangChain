from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

from langgraph.prebuilt import ToolRuntime

@tool
def get_weather(city: str, runtime:ToolRuntime) -> str:
    """获取给定城市的天气。"""
    return f"总是阳光灿烂 {city}!"

@tool
def call_weather(city: str) -> str:
    """调用天气工具获取给定城市的天气。"""
    result = subagent.invoke({"messages": [HumanMessage(city)]})
    return result["messages"][-1].text

agent = create_agent(
    model="deepseek-v4-pro",
    tools=[call_weather],
    name="supervisor",
)

subagent = create_agent(
    model="deepseek-v4-pro",
    tools=[get_weather],
    name="weather_agent",
)

stream = agent.stream_events(
    {"messages": [HumanMessage(content="济南市的天气怎么样")]},
           version="v3",
)


for agent in stream.subagents:
    print(f"sub_agent{agent.name}")
    for message in agent.messages:
        print(f"\n{message.output}")
# for message in stream.messages:
#     print(f"agent{agent.name}")
#     print(message.reasoning)
