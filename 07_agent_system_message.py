from pprint import pprint

from langchain.agents import create_agent
from langchain.agents.middleware import ModelRequest, ModelResponse, wrap_model_call
from langchain_core.messages import HumanMessage, SystemMessage

@wrap_model_call
def dynamic_system_message(request: ModelRequest, handler) -> ModelResponse:
    pprint(request)
    return handler(request.override(system_message=SystemMessage(content="你是一个翻译助手，能把我说的话全部转成英文")))

agent = create_agent(
    model="deepseek-v4-pro",
    system_prompt=SystemMessage(content="你是一个旅游规划助手，帮我做一个简短的旅游规划"),
    middleware=[dynamic_system_message]
)
response = agent.invoke(
    {"messages": HumanMessage(content="我想去杭州")}
)
pprint(response)