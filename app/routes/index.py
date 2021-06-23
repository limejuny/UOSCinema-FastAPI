from datetime import datetime

from fastapi import APIRouter
from starlette.responses import Response

from . import auth

router = APIRouter()


@router.get("/")
async def index():
    """
    상태 체크용 API  
    :return:
    """
    current_time = datetime.utcnow()
    return Response(
        f"Notification API (UTC: {current_time.strftime('%Y.%m.%d %H:%M:%S')})")


router.include_router(auth.router, tags=["Authentication"], prefix="/auth")
