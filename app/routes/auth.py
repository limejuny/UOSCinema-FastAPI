import jwt
from hashlib import sha256

from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.database.models import UserLogin
from app.database.schema import Usr
from app.common.const import (JWT_SECRET, JWT_ALGORITHM)

router = APIRouter()


@router.post("/login")
async def index(account: UserLogin):
    """
    로그인 API  
    :return:
    """
    usr: Usr = Usr.get(usr_id=account.userId)
    res = JSONResponse(status_code=401, content="아이디 또는 비밀번호를 다시 확인해주세요.")
    if not usr:
        return res
    passwd = sha256(account.password.encode()).hexdigest()
    if passwd != usr.usr_password:
        return res
    res = {
        'userId': usr.usr_id,
        'userName': usr.usr_name,
        'email': usr.usr_email,
        'isAdmin': usr.usr_type == 0
    }
    token: str = jwt.encode(res, JWT_SECRET, JWT_ALGORITHM)
    res = JSONResponse(res, status_code=200)
    res.set_cookie(key='jwt', value=token, httponly=False)
    return res
