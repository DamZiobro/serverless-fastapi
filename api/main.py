"""Main file of the FastAPI simple app."""
import os

from fastapi import FastAPI
from mangum import Mangum

stage = os.environ.get("STAGE", None)
openapi_prefix = f"/{stage}" if stage else "/"

app = FastAPI(title="serverless-fastapi", openapi_prefix=openapi_prefix)


@app.get("/hello")
def hello():
    """GET /hello endpoint."""
    return {"message": "Hello World"}


handler = Mangum(app)  # handler for deploy FastAPI to lambdas
