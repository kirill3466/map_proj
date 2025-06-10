from typing import List, Optional

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import JSONResponse

from auth.views import auth_router, user_router
from document.views import router as document_router
from notification.views import router as notification_router
from parcel.views import router as parcel_router
from poll.views import router as poll_router
from post.views import router as post_router
from ticket.views import router as ticket_router


class ErrorMessage(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    detail: Optional[List[ErrorMessage]]


api_router = APIRouter(
    default_response_class=JSONResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)

api_router.include_router(
    parcel_router,
    prefix="/parcels",
    tags=["parcels"]
)

api_router.include_router(
    ticket_router,
    prefix="/tickets",
    tags=["tickets"]
)

api_router.include_router(
    user_router,
    prefix="/users",
    tags=["users"]
)

api_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["auth"]
)

api_router.include_router(
    poll_router,
    prefix="/polls",
    tags=["polls"]
)


api_router.include_router(
    document_router,
    prefix="/documents",
    tags=["documents"]
)


api_router.include_router(
    notification_router,
    prefix="/notifications",
    tags=["notifications"]
)

api_router.include_router(
    post_router,
    prefix="/posts",
    tags=["posts"]
)


@api_router.get("/isalive", include_in_schema=False)
async def is_alive() -> dict:
    return {"alive": True}
