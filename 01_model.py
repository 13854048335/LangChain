import os
from langchain_deepseek import ChatDeepSeek
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from langchain.messages import HumanMessage, AIMessage, SystemMessage


api_key = os.getenv("DEEPSEEK_API_KEY")
# conversation = [
#     {"role": "system", "content": "你是一个旅游规划助手，最多输出200个字"},
#     {"role": "user", "content": "我想去天津玩一天"},
#     {"role": "assistant", "content": "天津太热别去了"},
#     {"role": "user", "content": "我想去武汉玩一天"}
# ]
conversation = [
    SystemMessage("你是一个旅游规划助手，最多输出200个字"),
    HumanMessage("我想去天津玩一天"),
    AIMessage("天津太热别去了"),
    HumanMessage("我想去武汉玩一天")
]
# llm = ChatOpenAI(
#             model="deepseek-v4-pro",
#             temperature=0,
#             max_tokens=None,
#             timeout=None,
#             max_retries=2,
#             api_key=SecretStr("sk-db0544ca7f784dbbac9fc00469aefb0e"),
#             base_url="https://api.deepseek.com",
#         )
llm = init_chat_model(
        model="deepseek-v4-pro",
        temperature=2,
        max_tokens=1024,
        timeout=20,
        max_retries=6,
        base_url="https://api.deepseek.com",
)
# llm = ChatDeepSeek(
#     model="deepseek-v4-pro",
#     temperature=0,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2,
#     # other params...
# )
#ai_msg = llm.stream(conversation)
#
# The
# The sky
# The sky is
# The sky is typically
# The sky is typically blue
# ...

#
# [{"type": "text", "text": "The sky is typically blue..."}]
responses = llm.batch([
    "1+1 = ?",
    "中国的首都是哪",
    "榴莲是不是水果"
])
for response in responses:
    print(response)