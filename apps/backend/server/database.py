import motor.motor_asyncio
from bson.objectid import ObjectId
import os


IS_CI = os.getenv("CI", "false") == "true"
MONGO_DETAILS = os.getenv(
"MONGODB_URL", 
    "mongodb://localhost:42069/?replicaSet=test-rs" if IS_CI else "mongodb://localhost:27017"
)

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.rescue_firstResponder

firstResponder_collection = database.get_collection("rescue_firstResponder")

firstResponder_collection.create_index("email", unique=True)

def firstResponder_helper(firstResponder) -> dict:
    return {
        "id": str(firstResponder["_id"]),
        "fullname": firstResponder["fullname"],
        "email": firstResponder["email"],
        "designation": firstResponder["designation"],
        "service": firstResponder["service"],
        "age": firstResponder["age"],
    }

# Retrieve all students present in the database
async def retrieve_firstResponders():
    firstResponders = []
    async for student in firstResponder_collection.find():
        firstResponders.append(firstResponder_helper(student))
    return firstResponders


# Add a new student into to the database
async def add_firstResponder(firstResponders_data: dict) -> dict:
    firstResponder = await firstResponder_collection.insert_one(firstResponders_data)
    new_firstResponder = await firstResponder_collection.find_one({"_id": firstResponder.inserted_id})
    return firstResponder_helper(new_firstResponder)


# Retrieve a student with a matching ID
async def retrieve_firstResponder(id: str) -> dict:
    firstResponder = await firstResponder_collection.find_one({"_id": ObjectId(id)})
    if firstResponder:
        return firstResponder_helper(firstResponder)


# Update a student with a matching ID
async def update_firstResponder(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    firstResponder = await firstResponder_collection.find_one({"_id": ObjectId(id)})
    if firstResponder:
        updated_firstResponder = await firstResponder_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_firstResponder:
            return True
        return False


# Delete a student from the database
async def delete_firstResponder(id: str):
    student = await firstResponder_collection.find_one({"_id": ObjectId(id)})
    if student:
        await firstResponder_collection.delete_one({"_id": ObjectId(id)})
        return True

