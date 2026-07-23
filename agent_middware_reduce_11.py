from typing import Annotated, Callable
from pprint import pprint
from langchain.agents.middleware import (
    wrap_tool_call,
    AgentMiddleware,
    AgentState,
    ExtendedModelResponse,
    ModelRequest,
    ModelResponse
)
from langchain.messages import SystemMessage
from langgraph.types import Command
from typing_extensions import NotRequired
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage, HumanMessage


def _last_wins(_a: str, b: str) -> str:
    """Reducer: last writer wins (outer overwrites inner)."""
    print(f"_a {_a}  _b  {b}")
    return b


class CustomMiddlewareState(AgentState):
    """Agent state: trace_layer uses last-wins (outer wins), messages use additive reducer."""

    # Non-reducer field with last-wins: both middleware write; outermost value wins
    trace_layer: NotRequired[Annotated[str, _last_wins]]


class OuterMiddleware(AgentMiddleware):
    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ExtendedModelResponse:

        pprint("OuterMiddleware_before")
        response = handler(request)
        pprint("OuterMiddleware_after")
        return ExtendedModelResponse(
            model_response=response,
            command=Command(update={
                "trace_layer": "outer",
                "messages": [SystemMessage(content="[Outer ran]")],
            }),
        )


class InnerMiddleware(AgentMiddleware):
    """Adds trace_layer and message. Outer adds to same keys; trace_layer: outer wins, messages: additive."""

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ):
        pprint("InnerMiddleware_before")
        response = handler(request)
        pprint("InnerMiddleware_after")
        return ExtendedModelResponse(
            model_response=response,
            command=Command(update={
                "trace_layer": "inner",
                "messages": [SystemMessage(content="[Inner ran]")],
            }),
        )
agent = create_agent(
    model="deepseek-v4-pro",
    system_prompt=SystemMessage(content="你是一个旅游规划助手，帮我做一个旅游规划，用言简意赅简短的语言回答"),
    middleware=[OuterMiddleware(), InnerMiddleware()],
    state_schema=CustomMiddlewareState
)
response = agent.invoke(
    {
        "messages": [HumanMessage(content="我要去杭州玩一天")],
        "model_call_count" :0
    }
)
pprint(response)