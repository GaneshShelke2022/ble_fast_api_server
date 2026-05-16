from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies import get_current_user
from ..database import get_async_session
from ..services.board_service import list_boards, create_board, update_board, delete_board
from ..schemas.board_schema import BoardCreate, BoardOut
from ..utils.response import success_response, error_response

router = APIRouter(prefix="/boards", tags=["boards"])


@router.get("")
async def get_boards(db: AsyncSession = Depends(get_async_session), user=Depends(get_current_user)):
    boards = await list_boards(db)
    return boards


@router.post("")
async def add_board(data: BoardCreate, db: AsyncSession = Depends(get_async_session), user=Depends(get_current_user)):
    try:
        payload = data.dict()
        b, err = await create_board(db, **payload)
        if err:
            return error_response(err)
        return success_response("Board added", BoardOut.from_orm(b).dict())
    except Exception as e:
        return error_response(str(e))


@router.put("/{board_id}")
async def edit_board(board_id: int, data: BoardCreate, db: AsyncSession = Depends(get_async_session), user=Depends(get_current_user)):
    b = await update_board(db, board_id, **data.dict())
    if not b:
        raise HTTPException(status_code=404, detail="Board not found")
    return success_response("Board updated", BoardOut.from_orm(b).dict())


@router.delete("/{board_id}")
async def remove_board(board_id: int, db: AsyncSession = Depends(get_async_session), user=Depends(get_current_user)):
    ok = await delete_board(db, board_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Board not found")
    return success_response("Board deleted", None)
