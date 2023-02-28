from fastapi import FastAPI

from server.routes.users import router as UserRouter
from server.routes.openstack import router as OpenRouter
from server.routes.nats import router as NatsRouter
from server.routes.websocket import router as WebsocketRouter

app = FastAPI()
app.include_router(OpenRouter, tags=["open"], prefix="/open")
app.include_router(UserRouter, tags=["user"], prefix="/user")
app.include_router(NatsRouter, tags=["nats"], prefix="/nats")
app.include_router(WebsocketRouter, tags=["socket"], prefix="/socket")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
