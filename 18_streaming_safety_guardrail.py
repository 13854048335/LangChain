from typing import Any, Literal
from langchain.agents.middleware import after_agent, AgentState
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_deepseek import ChatDeepSeek
from langgraph.runtime import Runtime
from langchain.messages import AIMessage
from langgraph.config import get_stream_writer
from pydantic import BaseModel


class ResponseSafety(BaseModel):
    """Evaluate a response as safe or unsafe."""
    evaluation: Literal["safe", "unsafe"]


llm = ChatDeepSeek(
    model="deepseek-v4-pro",
    temperature=0,
    extra_body={"thinking": {"type": "disabled"}}
)

@after_agent(can_jump_to=["end"])
def safety_guardrail(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """基于模型的护栏：使用LLM评估响应安全性"""
    stream_writer = get_stream_writer()
    # Get the model response
    if not state["messages"]:
        return None

    last_message = state["messages"][-1]
    if not isinstance(last_message, AIMessage):
        return None

    # Use another model to evaluate safety
    model_with_tools = llm.bind_tools([ResponseSafety], tool_choice="any")
    result = model_with_tools.invoke(
        [
            SystemMessage("将此AI响应评估为一般安全或不安全。"),
            HumanMessage(f"AI response: {last_message.text}")
        ]
    )
    stream_writer(result)

    tool_call = result.tool_calls[0]
    if tool_call["args"]["evaluation"] == "unsafe":
        last_message.content = "我不能提供这种答复。请重新表述您的请求。"

    return None