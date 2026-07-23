from pprint import pprint
from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware, AgentState, hook_config
from langchain.messages import AIMessage
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.runtime import Runtime
from typing import Any
from langchain.agents.middleware import AgentMiddleware, ModelRequest, ModelResponse
from typing import Callable
# class MessageLimitMiddleware(AgentMiddleware):
#     def __init__(self, max_messages: int = 50):
#         super().__init__()
#         self.max_messages = max_messages
#
#     @hook_config(can_jump_to=["end"])
#     def before_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
#         print("Before Model")
#         if len(state["messages"]) >= self.max_messages:
#             return {
#                 "messages": [AIMessage("Conversation limit reached.")],
#                 "jump_to": "end"
#             }
#         return None
#
#     def after_model(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
#         print(f"Model returned: {state['messages'][-1].content}")
#         return None

class RetryMiddleware(AgentMiddleware):
    def __init__(self, max_retries: int = 3):
        super().__init__()
        self.max_retries = max_retries

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        for attempt in range(self.max_retries):
            try:
                return handler(request)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise
                print(f"Retry {attempt + 1}/{self.max_retries} after error: {e}")
agent = create_agent(
    model="deepseek-v4-pro",
    system_prompt=SystemMessage(content="你是一个旅游规划助手，帮我做一个简短的旅游规划"),
    middleware=[RetryMiddleware()]
)
response = agent.invoke(
    {"messages": HumanMessage(content="我要去杭州玩一天")}
)
pprint(response)
