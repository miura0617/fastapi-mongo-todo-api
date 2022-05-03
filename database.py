##############################
# MongoDBと連携する処理
##############################
from decouple import config
from typing import Union
import motor.motor_asyncio
from bson import ObjectId


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

async def db_get_todos() -> list:
    todos = []
    for todo in await collection_todo.find().to_list(length=100):
        todos.append(todo_serializer(todo))
    return todos

async def db_get_single_todo(id: str) -> Union[dict, bool]:
    # MongoDBのDB内部ではbsonというデータ型で保存されている
    todo = await collection_todo.find_one({"_id": ObjectId(id)})
    if todo:
        return todo_serializer(todo)
    return False

async def db_update_todo(id: str, data: dict) -> Union[dict, bool]:
    # idのタスクがあるか確認
    todo = await collection_todo.find_one({"_id": ObjectId(id)})
    if todo:
        # update_oneメソッドの戻り値は、UpdateResultクラスのインスタンスになる
        # UpdateResultクラスのmodified_count属性が更新できた数を示す
        updated_todo = await collection_todo.update_one(
            {"_id": ObjectId(id)},
            {"$set": data}
        )
        if  (updated_todo.modified_count > 0):
            new_todo = await collection_todo.find_one({"_id": ObjectId(id)})
            return todo_serializer(new_todo)
    return False


async def db_delete_todo(id: str) -> bool:
    todo = await collection_todo.find_one({"_id": ObjectId(id)})
    if todo:
        # delete_oneメソッドの戻り値は、DeleteResultクラスのインスタンス
        # DeleteResultクラスのdeleted_count属性を持つ
        deleted_todo = await collection_todo.delete_one({"_id": ObjectId(id)})
        if (deleted_todo.deleted_count > 0):
            return True
    return False
    