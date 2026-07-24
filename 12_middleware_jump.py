from pprint import pprint
from langchain.agents import create_agent
from langchain.agents.middleware import AgentState, hook_config
from langchain.messages import AIMessage
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.runtime import Runtime
from typing import Any
from langchain.agents.middleware import AgentMiddleware
from typing_extensions import NotRequired


class AnswerCheckState(AgentState):
    # 记录已经要求模型回答多少次
    rewrite_count: NotRequired[int]

class AnswerCheckMiddleware(
    AgentMiddleware[AnswerCheckState]
):
    state_schema = AgentState
    @hook_config(can_jump_to=["model"])
    def after_agent(
            self,
            state: AnswerCheckState,
            runtime:Runtime
    ) -> dict[str, Any] | None:
        last_message = state["messages"][-1]
        rewrite_count = state.get("rewrite_count", 0)

        #只检查模型生成的消息
        if not isinstance(last_message, AIMessage):
            return  None
        answer = last_message.text
        if len(answer) > 50 and rewrite_count < 1:
            return{
                # 向对话中追加一条重新回答的要求
                "messages": [HumanMessage("刚才的回答有点复杂请给出更简洁的回答")],
                # 更新重新回答的次数
                "rewrite_count": rewrite_count + 1,
                # 跳回模型节点
                "jump_to": "model"
            }
        # 回答合格，或者已经重新生成了一次正常结束
        return None

agent = create_agent(
    model="deepseek-v4-pro",
    system_prompt=SystemMessage(content="你是一个数学老师"),
    middleware=[AnswerCheckMiddleware()],
    state_schema=AnswerCheckState
)
response = agent.invoke(
    {"messages": HumanMessage(content="给我讲解一下数学的逻辑")}
)
pprint(response)