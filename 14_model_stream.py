from langchain_deepseek import ChatDeepSeek
from langchain.tools import tool


@tool
def get_weather(location: str) -> str:
    """Search for information."""
    return f"{location}这个城市的天气每天都晴朗"

llm = ChatDeepSeek(
    model="deepseek-v4-pro",
    #extra_body={"thinking": {"type": "disabled"}}
)

llm_with_tools = llm.bind_tools([get_weather])

reasoning_content = ""
llm_count = ""
tool_calls = []
for chunk in llm_with_tools.stream("北京的天气如何?"):
    if chunk.additional_kwargs:
        reasoning_content += chunk.additional_kwargs.get("reasoning_content")
    if chunk.content:
        llm_count += chunk.content
    if chunk.tool_calls:
        for index, tool_call in enumerate(chunk.tool_calls):
            if tool_call["name"]: tool_calls.append({"tool_name": tool_call["name"]})


print(f"正在思考: {reasoning_content}")
if llm: print(f"LLM输出: {llm_count}")
print(f"工具调用: {tool_calls}")

