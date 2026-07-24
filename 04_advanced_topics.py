from langchain.agents.middleware import wrap_model_call
from langchain.messages import HumanMessage
from langchain_deepseek import ChatDeepSeek
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
import base64
from io import BytesIO
from PIL import Image
from langchain.agents import create_agent
# from langchain_ollama import ChatOllama
#
# llm = ChatOllama(
#     model="deepseek-r1:1.5b",
#     temperature=0,
#     # other params...
# )
# messages = [
#     (
#         "system",
#         "你是旅游规划助手",
#     ),
#     ("human", "我想去日本大阪。"),
# ]
# ai_msg = llm.invoke(messages)
# print(ai_msg.text)
def convert_to_base64(pil_image):
    """
    Convert PIL images to Base64 encoded strings

    :param pil_image: PIL image
    :return: Re-sized Base64 string
    """
    buffered = BytesIO()
    pil_image.save(buffered, format="JPEG")  # You can change the format if needed
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str
ollama = ChatOllama(model="modelscope.cn/unsloth/Qwen3.5-4B-GGUF:latest", temperature=0)
deepseek = ChatDeepSeek(
    model="deepseek-v4-pro",
    temperature=0,
 )
file_path = "C:\\Users\\16786\\Pictures\\截图\\123.jpeg"
pil_image = Image.open(file_path)

image_b64 = convert_to_base64(pil_image)


def prompt_func(data):
    text = data["text"]
    image = data["image"]

    image_part = {
        "type": "image_url",
        "image_url": f"data:image/jpeg;base64,{image}",
    }

    content_parts = []

    text_part = {"type": "text", "text": text}

    content_parts.append(image_part)
    content_parts.append(text_part)

    return [HumanMessage(content=content_parts)]
message_a = prompt_func({"text": "这张图片当中有几个人?", "image": image_b64})
message_b = [
    HumanMessage(content="你是什么模型?"),
]
def contains_image(messages):
    # 多模态Content是一个列表
    for msg in messages:
        if isinstance(getattr(msg, "content", None), list):
            for part in msg.content:
                if isinstance(part, dict) and part.get("type") == "image_url":
                    return True
    return False

@wrap_model_call
def dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse:
    """Choose model based on conversation complexity."""
    # message_count = len(request.state["messages"])
    # print("Message count:", request)
    contains_image_flag = contains_image(request.state["messages"])
    if contains_image_flag:
        # Use an advanced model for longer conversations
        model = ollama
    else:
        model = deepseek

    return handler(request.override(model=model))

# chain = prompt_func | ollama | StrOutputParser()
#
# query_chain = chain.invoke(
#     {"text": "这张图片当中有几个人?", "image": image_b64}
# )
agent = create_agent(
    model=ollama,  # Default model
    middleware=[dynamic_model_selection]
)
response = agent.invoke(
    {"messages": message_b},
)
print(response['messages'][1].content)