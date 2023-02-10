import motor.motor_asyncio
from bson.objectid import ObjectId


MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

userdatabase = client.users

user_collection = userdatabase.get_collection("users_collection")


# Retrieve all users present in the database
async def retrieve_users():
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users


# Add a new user into to the database
async def add_user(user_data: dict) -> dict:
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)


# Retrieve a user with a matching ID
async def retrieve_user(username: str) -> dict:
    user = await user_collection.find_one({"username": ObjectId(username)})
    if user:
        return user_helper(user)



def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "password": user["password"]
    }