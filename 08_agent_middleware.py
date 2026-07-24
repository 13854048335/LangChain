from pprint import pprint
from typing import Callable
from langchain.agents import create_agent
from langchain.agents.middleware import before_agent, wrap_model_call, ModelResponse, ModelRequest, wrap_tool_call, \
    after_model, after_agent, before_model
from langchain_core.messages import ToolMessage, SystemMessage, HumanMessage
from langgraph.prebuilt.tool_node import ToolCallRequest
from langchain.agents import AgentState
from langgraph.runtime import Runtime
from langchain.tools import tool



@before_agent
def before_agent(state: AgentState, runtime: Runtime):
    print("Before Agent")

@before_model
def bef_model(state: AgentState, runtime: Runtime):
    print("Before Model")

@wrap_model_call
def wrap_model_call(request: ModelRequest, handler) -> ModelResponse:
    print("wrap_model_call")
    response = handler(request)
    pprint(f"wrap_model_call {response}")
    return handler(request)

@wrap_tool_call
def wrap_tool_call(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage],
) -> ToolMessage:
    print("wrap_tool_call")
    response =  handler(request)
    pprint(f"wrap_tool_call {response}")
    return response

@after_model
def after_model(state: AgentState, runtime: Runtime):
    print("After Model")

@after_agent
def after_agent(state: AgentState, runtime: Runtime):
    print("After Agent")

@tool
def search_location(location: str):
    """Search for information."""
    return f"Results for: {location}"

agent = create_agent(
    model="deepseek-v4-pro",
    system_prompt=SystemMessage(content="你是一个旅游规划助手，帮我做一个简短的旅游规划"),
    middleware=[before_agent, bef_model, wrap_model_call, wrap_tool_call, after_model, after_agent],
    tools=[search_location]
)
response = agent.invoke(
    {"messages": HumanMessage(content="我要去杭州玩一天")}
)
pprint(response)
