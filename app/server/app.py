from fastapi import FastAPI

from server.routes.users import router as UserRouter
from server.routes.openstack import router as OpenRouter

app = FastAPI()
app.include_router(OpenRouter, tags=["open"], prefix="/open")
app.include_router(UserRouter, tags=["user"], prefix="/user")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}