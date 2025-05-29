import asyncio as aio

from contextlib import asynccontextmanager
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(_: FastAPI):
    from hubitat_mcp.server import mcp

    aio.create_task(mcp.run_async("stdio"))

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/he_event")
def handle_device_event():
    # TODO: Implement Hubitat event handling
    pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
