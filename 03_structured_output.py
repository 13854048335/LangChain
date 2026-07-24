import json
from typing import List

from langchain_deepseek import ChatDeepSeek
from pydantic import BaseModel, Field
from typing_extensions import TypedDict, Annotated

llm = ChatDeepSeek(
    model="deepseek-v4-pro",
    extra_body={"thinking": {"type": "disabled"}}
)


# info = "有一个同学叫张三，他是个男生，他两年前是16岁"
#
# messages = [
#     {"role": "system", "content": "你是一个学生信息提取工具，name，sex，age这些信息，请直接提取Json对象，不要些MarkBook文档,不要输出其他任何内容"},
#     {"role": "user", "content": info},
# ]
# res = llm.invoke(messages)
# dict = json.loads(res.text)
# print(dict)
# print(type(dict))
class Movie(BaseModel):
    """一部带有详细信息的电影。"""
    title: str = Field(description="电影的标题")
    year: int = Field(gt=2020,description="电影发行的年份")
    director: str = Field(description="电影的导演")
    rating: float = Field(description="电影的评分(满分10分)")
class Student(BaseModel):
    """一个学生。"""
    name: str = Field(description="学生的名字")
    age: int = Field(gt=17,description="学生年龄")
class Teacher(BaseModel):
    """一个老师。"""
    name: str = Field(description="老师的名字")
    age: int = Field(description="老师年龄")
    students: List[Student]

# model_with_structure = llm.with_structured_output(Movie)
# response = model_with_structure.invoke("请提供关于电影《盗梦空间》的详细信息")
#print(response)  # Movie(title="Inception", year=2010, director="Christopher Nolan", rating=8.8)
# class MovieDict(TypedDict):
#     """一部带有详细信息的电影"""
#     title: Annotated[str, ..., "电影的标题"]
#     year: Annotated[int, ..., "电影发行的年份"]
#     director: Annotated[str, ..., "电影的导演"]
#     rating: Annotated[float, ..., "影的评分(满分10分)"]

# model_with_structure = llm.with_structured_output(Movie, include_raw=True)
# response = model_with_structure.invoke("请提供关于电影《战狼》的详细信息")
model_with_structure = llm.with_structured_output(Teacher, include_raw=True)
response = model_with_structure.invoke("有一个老师叫张三，年龄30岁,他有三个学生小李，小王，小张，其中小张和小王18岁，小李19岁")
print(response.get("parsed"))  # {'title': 'Inception', 'year': 2010, 'director': 'Christopher Nolan', 'rating': 8.8}
