from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ..auth.jwt_handler import create_access_token
from ..auth.password_handler import verify_password, get_password_hash
from ..database import AsyncSession, get_async_session
from ..utils.response import success_response, error_response
from sqlalchemy.future import select
from ..models import user_model

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
async def login(data: LoginRequest, db: AsyncSession = Depends(get_async_session)):
    try:
        # static test login support: if username == kipl and password == 123
        if data.username == "kipl" and data.password == "123":
            token = create_access_token(subject=data.username)
            return success_response("Login success", {"access_token": token})

        # otherwise try DB
        q = await db.execute(select(user_model.User).where(user_model.User.username == data.username))
        user = q.scalars().first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        if not verify_password(data.password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        token = create_access_token(subject=user.username)
        return success_response("Login success", {"access_token": token})
    except HTTPException:
        raise
    except Exception as e:
        return error_response(str(e))
