import asyncio

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

    # if chunk["type"] == "messages":
    #     token, metadata = chunk["data"]
    #     print(f"node: {metadata['langgraph_node']}")
    #     print(f"content: {token.content_blocks}")
    #     print("\n")
async def main():
    async for chunk in agent.astream(
        {"messages": [HumanMessage("济南的天气如何")]},
        stream_mode=["updates","messages","custom"],
        version="v2"
    ):
        #print(chunk)
        chunk_type = chunk["type"]
        data = chunk["data"]
        if chunk_type == "messages":
            token,metadata = data
            if getattr(token, "content", None):
                print(token.content,end="",flush=True)
            elif getattr(token, "additional_kwargs", None):
                print(token.additional_kwargs.get("reasoning_content"),end="",flush=True)
        elif chunk_type == "updates":
            print(f"\n Updates:{data}")
        elif chunk_type == "custom":
            print(f"Custom:{data}")

if __name__ == "__main__":
    asyncio.run(main())
