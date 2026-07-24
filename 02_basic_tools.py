from langchain.chat_models import init_chat_model
from langchain.tools import tool

llm = init_chat_model(
        model="deepseek-v4-pro",
        temperature=2,
        max_tokens=1024,
        timeout=20,
        max_retries=6,
        base_url="https://api.deepseek.com",
        extra_body={"thinking": {"type": "disabled"}}
)
@tool
def get_weather(location: str) -> str:
    """获取某个地点的天气。"""
    print(f"正在获取 {location}的天气信息.")
    return f"正在获取 {location}的天气信息."


# @tool
# def search(location: str) -> str:
#     """根据地点名称获取对应的经纬度信息。"""
#     return f"经纬度信息{location}"


# model_with_tools = llm.bind_tools([get_weather])
#
# response = model_with_tools.invoke("What's the weather like in Boston?")
# for tool_call in response.tool_calls:
#     # 查看模型生成的工具调用
#     print(f"Tool: {tool_call['name']}")
#     print(f"Args: {tool_call['args']}")

# 将（可能多个）工具绑定到模型
# model_with_tools = llm.bind_tools([get_weather])
#
# # 步骤 1: 模型生成工具调用
# messages = [{"role": "user", "content": "What's the weather in Boston?"}]
# ai_msg = model_with_tools.invoke(messages)
# messages.append(ai_msg)
# print(1,messages)
#
# # 步骤 2: 执行工具并收集结果
# for tool_call in ai_msg.tool_calls:
#     # 使用生成的参数执行工具
#     print("tool_call",tool_call)
#     tool_result = get_weather.invoke(tool_call)
#     messages.append(tool_result)
# print(2,messages)
# # 步骤 3: 将结果传回模型以获得最终响应
# final_response = model_with_tools.invoke(messages)
# print(final_response.text)
# "The current weather in Boston is 72°F and sunny."

# 强制工具调用
# model_with_tools = llm.bind_tools([get_weather, search], tool_choice="search")
# res = model_with_tools.invoke("重庆今天天气怎么样")
# print(res.tool_calls)
model_with_tools = llm.bind_tools([get_weather])
#
# response = model_with_tools.invoke(
#     "What's the weather in 上海 and 北京?"
# )


# 并行工具调用
# print(response.tool_calls)
# [
#   {'name': 'get_weather', 'args': {'location': 'Boston'}, 'id': 'call_1'},
#   {'name': 'get_weather', 'args': {'location': 'Tokyo'}, 'id': 'call_2'},
# ]


# 执行所有工具（可以与async并行完成）
# results = []
# for tool_call in response.tool_calls:
#     if tool_call['name'] == 'get_weather':
#         result = get_weather.invoke(tool_call)
#     ...
#     results.append(result)
# print(results)

# 工具调用流式返回
for chunk in model_with_tools.stream(
    "What's the weather in 北京 and 上海"
):
    # 工具调用块逐步到达
    for tool_chunk in chunk.tool_call_chunks:
        if name := tool_chunk.get("name"):
            print(f"Tool: {name}")
        if id_ := tool_chunk.get("id"):
            print(f"ID: {id_}")
        if args := tool_chunk.get("args"):
            print(f"Args: {args}")

# Output:
# Tool: get_weather
# ID: call_SvMlU1TVIZugrFLckFE2ceRE
# Args: {"lo
# Args: catio
# Args: n": "B
# Args: osto
# Args: n"}
# Tool: get_weather
# ID: call_QMZdy6qInx13oWKE7KhuhOLR
# Args: {"lo
# Args: catio
# Args: n": "T
# Args: okyo
# Args: "}