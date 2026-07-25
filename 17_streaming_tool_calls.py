from pprint import pprint
from typing import Any

from langchain.agents import create_agent
from langchain.messages import AIMessage, AIMessageChunk, AnyMessage, ToolMessage
from langchain_core.messages import HumanMessage


def get_weather(city: str) -> str:
    """获取某个城市的天气"""
    """获取某个城市的天气"""
    return f"这里总是阳光明媚 {city}!"


agent = create_agent("deepseek-v4-pro", tools=[get_weather])


def _render_message_chunk(token: AIMessageChunk) -> None:
    if token.text:
        print(token.text, end="|")
    if token.tool_call_chunks:
        print(token.tool_call_chunks)
    # N.B. all content is available through token.content_blocks


def _render_completed_message(message: AnyMessage) -> None:
    if isinstance(message, AIMessage) and message.tool_calls:
        print(f"Tool calls: {message.tool_calls}")
    if isinstance(message, ToolMessage):
        print(f"Tool response: {message.content_blocks}")


for chunk in agent.stream(
    {"messages": [HumanMessage("北京今天天气怎么样?")]},
    stream_mode=["messages", "updates"],
    version="v2",
):
    print(chunk)
    if chunk["type"] == "messages":
        token, metadata = chunk["data"]
        #print(token)
        if isinstance(token, AIMessageChunk):
            _render_message_chunk(token)
    elif chunk["type"] == "updates":
        for source, update in chunk["data"].items():
            if source in ("model", "tools"):  # `source` captures node name
                _render_completed_message(update["messages"][-1])