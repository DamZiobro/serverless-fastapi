"""Implementation of Use Cases based on the Clean Architecture principles"""

import time

from fastapi import (
    FastAPI,
    Request,
)
from mangum import Mangum

from api import __version__
from api.routes.todo import router as todo_router


app = FastAPI(
    title="fastapi-react-serverless",
    version=__version__,
    openapi_url="/openapi.json",
    docs_url="/docs",
)
app.include_router(todo_router)


@app.get("/")
async def root():
    return {"message": "Hello TODOS API"}


handler = Mangum(app)  # handler for deploy FastAPI to lambdas


# add middleware which calculates time of the request processing
# and assign it to the response header
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time-Sec"] = str(process_time)
    return response
