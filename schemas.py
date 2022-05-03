##############################
# エンドポイントにわたすデータ型やレスポンスのデータ型を定義
##############################
from lib2to3.pytree import Base
from pydantic import BaseModel


class Todo(BaseModel):
    id: str
    title: str
    description: str

class TodoBody(BaseModel):
    title: str
    description: str

class SuccessMsg(BaseModel):
    message: str
