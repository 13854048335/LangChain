from langchain.tools import tool
from pprint import pprint
from langchain.agents import create_agent
from langchain.agents.middleware import AgentState, hook_config
from langchain.messages import AIMessage
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.runtime import Runtime
from typing import Any
from langchain.agents.middleware import AgentMiddleware
from typing_extensions import NotRequired

@tool
def search(param:str):
    """用来测试的工具"""
    return f"用来测试 {param}"

class AnswerCheckMiddleware(AgentMiddleware):
    state_schema = AgentState
    @hook_config(can_jump_to=["tools"])
    def before_model(
            self,
            state:AgentState,
            runtime:Runtime
    ) -> dict[str, Any] | None:
        last_message = state["messages"][-1]
        if not isinstance(last_message, HumanMessage):
            return None
        return{
            "messages": [
                AIMessage(content='',
                            id='lc_run--019f93f9-a362-7050-924d-5d28328ff182-0',
                            tool_calls=[{'name': 'search', 'args': {'param': '济南'}, 'id': 'call_00_RJtyRKdoq3aS8wvEVzkE3702', 'type': 'tool_call'}])
                ],
                "jump_to": "tools"
            }

agent = create_agent(
    model="deepseek-v4-pro",
    system_prompt=SystemMessage(content="你是一个旅游规划助手，帮我做一个旅游规划，用言简意赅简短的语言回答"),
    middleware=[AnswerCheckMiddleware()],
    tools=[search]
)
response = agent.invoke(
    {"messages": HumanMessage(content="我要去南京玩一天")}
)
pprint(response)