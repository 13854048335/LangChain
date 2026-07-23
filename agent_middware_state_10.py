from unittest import result
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.agents.middleware import after_model, before_model, AgentState
from langchain_core import messages
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.runtime import Runtime
from typing import Any
from typing_extensions import NotRequired
from pprint import pprint
from typing import Callable
from langchain.agents.middleware import (
    wrap_model_call,
    wrap_tool_call,
    ModelRequest,
    ModelResponse,
    AgentState,
    ExtendedModelResponse
)
from langgraph.types import Command
from typing_extensions import NotRequired
from langgraph.prebuilt.tool_node import ToolCallRequest

# class TrackingState(AgentState):
#     model_call_count: NotRequired[int]
#
# @after_model
# def increment_after_model(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
#     pprint(state)
#     return {"model_call_count": state.get("model_call_count", 0) + 1}
#
# @before_model
# def increment_before_model(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
#     pprint(state)
#     return {"model_call_count": state.get("model_call_count", 0) + 1}


class UsageTrackingState(AgentState):
    """Agent state with token usage tracking."""
    last_model_call_tokens: NotRequired[int]


@wrap_model_call(state_schema=UsageTrackingState)
def track_usage(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ExtendedModelResponse:
    pprint(f"wrap_tool_call {request.state.get('last_model_call_tokens')}")
    response = handler(request)
    return ExtendedModelResponse(
        model_response=response,
        command=Command(update={"last_model_call_tokens": 150}),
    )
@wrap_tool_call
def wrap_tool_call(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage],
) -> Command:
    pprint(f"wrap_tool_call {request.state.get('last_model_call_tokens')}")
    response =  handler(request)
    return Command(
        update={
            "last_model_call_tokens": 300,
            "messages": [response]
        }
    )
@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

agent = create_agent(
    model="deepseek-v4-pro",
    system_prompt=SystemMessage(content="你是一个旅游规划助手，帮我做一个旅游规划，用言简意赅简短的语言回答"),
    middleware=[track_usage,wrap_tool_call],
    tools=[search]
)
response = agent.invoke(
    {
        "messages": [HumanMessage(content="我要去杭州玩一天")],
        "model_call_count" :0
    }
)
pprint(response)