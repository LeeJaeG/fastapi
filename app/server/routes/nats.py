from fastapi import APIRouter, WebSocket
from pydantic import BaseModel, Field
import os
import asyncio
import json

import websockets
import nats
from nats.errors import TimeoutError, NoRespondersError
from server.models.users import (

    ResponseModel,

)

from server.database import (
    add_error,
)

# async def sub():

#     servers = os.environ.get("NATS_URL", "nats://localhost:4222").split(",")

#     nc = await nats.connect(servers=servers)
    
#     async def greet_handler(msg):

#         name = msg.subject[6:]
#         reply = f"error, {name}"
#         print("sub : !!msg!! ","subject ",msg.subject," data ",msg.data)
#         msg_dict = {'subject':msg.subject,'data':msg.data.decode("utf8"),}
        
#         print("mongodb error input!")
#         await add_error(msg_dict)
        
#         await msg.respond(reply.encode("utf8"))
        
#         await sub.drain()

#     sub = await nc.subscribe("error.*", cb=greet_handler)

async def sub(websocket):
    servers = os.environ.get("NATS_URL", "nats://localhost:4222").split(",")

    nc = await nats.connect(servers=servers)
    async def message_handler(msg):
        
        name = msg.subject[6:]
        reply = f"error, {name}"
        print("sub : !!msg!! ","subject ",msg.subject," data ",msg.data)
        msg_dict = {'subject':msg.subject,'data':msg.data.decode("utf8"),}
        
        print("mongodb error input!")
        await add_error(msg_dict)
        
        await msg.respond(reply.encode("utf8"))
        
        await websocket.send_text("error input")
        # await sid.drain()
        
    sid = await nc.subscribe("error.*", cb=message_handler)

    while True:
        await asyncio.sleep(1)



async def req():

    servers = os.environ.get("NATS_URL", "nats://localhost:4222").split(",")

    nc = await nats.connect(servers=servers)

    rep = None  # 변수 초기화
    try:
        rep = await nc.request("error.1", b'hiii', timeout=0.5)
    except nats.aio.errors.ErrTimeout:
        print("NATS request timed out")
    except Exception as e:
        print(f"Exception: {e}")
    if rep:
        print("Got a response:", rep.data.decode())

router = APIRouter()

@router.get("/nats")
async def get_req():
    # await sub()
    await req()
    # users = list_users(conn)
    # if users:
    #     return ResponseModel(users, "users data retrieved successfully")
    # return ResponseModel(users, "Empty list returned")

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    
    await websocket.accept()
    await sub(websocket)
    
    
    # while True:
    #     data = await websocket.receive_text()
    #     message = json.loads(data)
    #     print(message)
        # await websocket.send_text(f"Message text was: {msg_dict}")