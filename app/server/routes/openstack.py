from fastapi import APIRouter

import openstack

from server.models.users import (

    ResponseModel,

)

openstack.enable_logging(debug=False)

conn = openstack.connect(cloud='admin')
    
def list_users(conn):
    users = []
    print("List Users:")

    for user in conn.identity.users():  
        users.append(user)
        
    return users

router = APIRouter()

@router.get("/openstack")
async def get_openstack():
    users = list_users(conn)
    if users:
        return ResponseModel(users, "users data retrieved successfully")
    return ResponseModel(users, "Empty list returned")

