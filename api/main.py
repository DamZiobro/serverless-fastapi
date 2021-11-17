"""Main file of the FastAPI simple app."""
import os

from fastapi import APIRouter, FastAPI
from mangum import Mangum

from api import __version__

stage = os.environ.get("STAGE", "")
root_path = f"/{stage}" if stage else ""

router = APIRouter()


@router.get("/hello")
def hello():
    """GET /hello endpoint."""
    return {"message": "Hello World"}


@router.get("/")
def root():
    """GET / endpoint."""
    return {"message": f"API version: {__version__}"}


app = FastAPI(
    title="serverless-fastapi",
    version=__version__,
    openapi_url=root_path + "/openapi.json",
    docs_url=root_path + "/docs",
)
app.include_router(router, prefix=root_path)

handler = Mangum(app)  # handler for deploy FastAPI to lambdas
