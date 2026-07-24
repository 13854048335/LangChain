from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

agent = create_agent(model="deepseek-v4-pro")
response = agent.invoke(
    {"messages": HumanMessage(content="你好")}
)
for msg in response["messages"]:
    print(msg)