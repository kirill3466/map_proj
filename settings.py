from pathlib import Path

from fastapi.templating import Jinja2Templates
from starlette.config import Config
from starlette.staticfiles import StaticFiles

config = Config(".env")

templates = Jinja2Templates(directory="templates")
static_files = StaticFiles(
    directory=Path(__file__).parent.parent.absolute() / "src/static"
)
PARCEL_FULL_CODE = config("PARCEL_FULL_CODE", default="86:11:0501010:")
JWT_SECRET = config("JWT_SECRET", default="abc123")
JWT_ALG = config("JWT_ALG", default="HS256")
JWT_EXP = config("WT_EXP", cast=int, default=86400)
AUTHENTICATION_PROVIDER = config(
    "AUTHENTICATION_PROVIDER",
    default="auth-provider-basic"
)
