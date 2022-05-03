from fastapi import APIRouter
from fastapi import Request, Response, HTTPException
from fastapi.encoders import jsonable_encoder
from schemas import Todo, TodoBody
from database import db_create_todo
from starlette.status import HTTP_201_CREATED


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