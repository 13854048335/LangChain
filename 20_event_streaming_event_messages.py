from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

from langgraph.prebuilt import ToolRuntime


@tool
def get_weather(city: str, runtime:ToolRuntime) -> str:
    """获取给定城市的天气。"""
    runtime.emit_output_delta("正在查询天气...\n")
    return f"总是阳光灿烂 {city}!"

agent = create_agent(
    model="deepseek-v4-pro",
    tools=[get_weather]
)
stream = agent.stream_events(
    {"messages": [HumanMessage(content="济南市的天气怎么样")]},
           version="v3",
)



# for message in stream.messages:
    # print(f"[{message.node}] ", end="")
    # for delta in message.text:
    #     print(delta, end="", flush=True)

    # full_message = message.output
    #print(full_message)
    # usage = full_message.usage_metadata
    # if usage:
        #print(usage)
        # pass
    # for delta in message.reasoning:
    #     print(f"[thinking] {delta}", end="", flush=True)
    # #
    # for delta in message.text:
    #     print(delta, end="", flush=True)
    # for chunk in message.tool_calls:
    #     print(f"tool call chunk: {chunk}")
    #
    # finalized = message.tool_calls.get()
    # if finalized:
    #     print(f"finalized tool calls: {finalized}")
for call in stream.tool_calls:
    print(f"{call.tool_name}({call.input})")
    for delta in call.output_deltas:
        print(delta, end="", flush=True)
    print(call.output, call.error)