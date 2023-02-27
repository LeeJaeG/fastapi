from fastapi import APIRouter
from pydantic import BaseModel, Field
import os
import asyncio
import json


import nats
from nats.errors import TimeoutError, NoRespondersError
from server.models.users import (

    ResponseModel,

)

from server.database import (
    add_error,
)
async def main():

    servers = os.environ.get("NATS_URL", "nats://localhost:4222").split(",")

    nc = await nats.connect(servers=servers)
    
    async def greet_handler(msg):

        name = msg.subject[6:]
        reply = f"error, {name}"
        print("sub : !!msg!! ","subject ",msg.subject," data ",msg.data)
        msg_dict = {'subject':msg.subject,'data':msg.data.decode("utf8"),}
        
        print("mongodb error input!")
        await add_error(msg_dict)
        
        await msg.respond(reply.encode("utf8"))

    sub = await nc.subscribe("error.*", cb=greet_handler)
    
    rep = await nc.request("error.1", b'hiii', timeout=0.5)
    
    print("response sub : ",f"{rep.data}")

router = APIRouter()

@router.get("/nats")
async def get_openstack():
    await main()
    # users = list_users(conn)
    # if users:
    #     return ResponseModel(users, "users data retrieved successfully")
    # return ResponseModel(users, "Empty list returned")

