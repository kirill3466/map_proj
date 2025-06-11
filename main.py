from contextvars import ContextVar
from typing import Final, Optional
from uuid import uuid1

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import scoped_session, sessionmaker
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from auth.auth import CurrUser

from parcel.bulk_create import bulk_create_parcels
import os
from db.core import engine
from routing import api_router
from settings import static_files, templates

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     process =
#     yield
#     process.terminate()


api = FastAPI(
    title="map-api",
)


api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


REQUEST_ID_CTX_KEY: Final[str] = "request_id"
_request_id_ctx_var: ContextVar[Optional[str]] = ContextVar(
    REQUEST_ID_CTX_KEY, default=None
)


def get_request_id() -> Optional[str]:
    return _request_id_ctx_var.get()


@api.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request_id = str(uuid1())
    ctx_token = _request_id_ctx_var.set(request_id)
    try:
        session = scoped_session(
            sessionmaker(bind=engine),
            scopefunc=get_request_id
        )
        request.state.db = session()
        response = await call_next(request)
    except Exception as e:
        raise e from None
    finally:
        request.state.db.close()
    _request_id_ctx_var.reset(ctx_token)
    return response


# закидывает jwt токен в заголовок Authorization
async def auth_middleware(request: Request, call_next):
    token = request.cookies.get("access_token")
    if token and token.startswith("Bearer "):
        token = token.split(" ")[1]
        request.headers.__dict__["_list"].append(
            (b"authorization", f"Bearer {token}".encode())
        )
    response = await call_next(request)
    return response

api.include_router(api_router)


@api.get("/")
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@api.get("/map")
async def map(request: Request, current_user: CurrUser):
    return templates.TemplateResponse("map.html", {"request": request})


@api.middleware("http")
async def redirect_unauthorized(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == 401:
        return RedirectResponse(url="auth/login")
    return response


# @api.get("/callback")
# async def callback(request: Request):
#     token = await

@api.on_event("startup")
def on_startup():
    from db.core import Base, engine
    Base.metadata.create_all(bind=engine)
    bulk_create_parcels(
        os.path.dirname(
            os.path.abspath(__file__)
        ) + "/static/geodata/result1.geojson"
    )


api.mount("/static", static_files, name="static")
api.add_middleware(GZipMiddleware)
api.middleware("http")(auth_middleware)


if __name__ == "__main__":
    uvicorn.run(api, host="0.0.0.0", port=8000, reload=True)
