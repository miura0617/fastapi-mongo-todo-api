##############################
# MongoDBと連携する処理
##############################
from decouple import config
from typing import Union
import motor.motor_asyncio


MONGO_API_KEY = config('MONGO_API_KEY')

# クライントを準備
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_API_KEY)
# MongoDBとコレクションをFastAPIで使えるようにする
# API_DBは、MongoDBのDB名
# todoとuserは、MongoDBの中のコレクション2つ
database = client.API_DB
collection_todo = database.todo
collection_user = database.user


def todo_serializer(todo) -> dict:
    return {
        "id": str(todo["_id"]),
        "title": todo["title"],
        "description": todo["description"]
    }

async def db_create_todo(data: dict) -> Union[dict, bool]:
    # motorのinsert_oneメソッドを使う
    todo = await collection_todo.insert_one(data)
    # insert_oneメソッドの戻り値はInsertOneResultというクラスのインスタンスになる
    # InsertOneResultクラスは、inserted_id属性を持ち、この属性でIDを取得できる
    new_todo = await collection_todo.find_one({"_id": todo.inserted_id})
    if new_todo:
        # new_todoの中のidは、MongoDBのObjectIDクラスから作られた特殊なIDになっている
        return todo_serializer(new_todo)
    return False