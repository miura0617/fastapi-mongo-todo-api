from fastapi import APIRouter
from fastapi import Request, Response, HTTPException
from fastapi.encoders import jsonable_encoder
from schemas import Todo, TodoBody, SuccessMsg
from database import db_create_todo, db_get_todos, db_get_single_todo, db_update_todo, db_delete_todo
from starlette.status import HTTP_201_CREATED
from typing import List


router = APIRouter()


@router.post("/api/todo", response_model=Todo)
async def create_todo(request: Request, response: Response, data: TodoBody):
    # リクエストボディはJSON型であり、データベースに書き込むときはdict型で書き込むので変換が必要
    # そのための関数がFastAPIに準備されている
    todo = jsonable_encoder(data)
    res = await db_create_todo(todo)
    # FastAPIでAPI実行が成功すると通常200だが
    # create操作なので201を返すように上書き
    response.status_code = HTTP_201_CREATED
    if res:
        return res
    raise HTTPException(
        status_code=404,
        detail="Create task failed"
    )

# タスク一覧取得用API
@router.get("/api/todo", response_model=List[Todo])
async def get_todos():
    res = await db_get_todos()
    return res

@router.get("/api/todo/{id}", response_model=Todo)
async def get_single_todo(id: str):
    res = await db_get_single_todo(id)
    if res:
        return res
    raise HTTPException(
        status_code=404,
        detail=f"Task of ID:{id} doesn't exist"
    )

@router.put("/api/todo/{id}", response_model=Todo)
async def update_todo(id: str, data: TodoBody):
    todo = jsonable_encoder(data)
    res = await db_update_todo(id, todo)
    if res:
        return res
    raise HTTPException(
        status_code=404,
        detail="Update task failed"
    )

@router.delete("/api/todo/{id}", response_model=SuccessMsg)
async def delete_todo(id: str):
    res = await db_delete_todo(id)
    if res:
        return {"message": "Successfully deleted"}
    raise HTTPException(
        status_code=404,
        detail="Delete task failed"
    )