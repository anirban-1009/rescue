"""Module handling the First Responder Database interaction"""

from bson.objectid import ObjectId
from typing import Optional

from src.data_utils.baseHandler import BaseMongoHandler
from src.first_responders.model import FirstResponder


class FirstResponderHandler(BaseMongoHandler):
    """Object handling the db instance of the first responder."""

    def __init__(self):
        super().__init__()

        self.collection = self.database.get_collection("FirstResponder")
        self.collection.create_index("email", unique=True)

    async def retrive_firstResponder(self):
        """Retrieve all students present in the database"""
        firstResponders = []
        async for student in self.collection.find():
            firstResponders.append(FirstResponder.model_validate(student))
        return firstResponders

    async def add_firstResponder(self, firstResponders_data: dict) -> dict:
        """Add a new student into to the database"""
        firstResponder = await self.collection.insert_one(firstResponders_data)
        new_firstResponder = await self.collection.find_one(
            {"_id": firstResponder.inserted_id}
        )
        return FirstResponder.model_validate(new_firstResponder)

    async def retrieve_firstResponder(self, id: str) -> Optional[FirstResponder]:
        """Retrieve a student with a matching ID"""
        firstResponder = await self.collection.find_one({"_id": ObjectId(id)})
        if firstResponder:
            return FirstResponder.model_validate(firstResponder)
        return None

    async def update_firstResponder(self, id: str, data: dict) -> bool:
        """Return false if an empty request body is sent."""
        if len(data) < 1:
            return False
        firstResponder = await self.collection.find_one({"_id": ObjectId(id)})
        if firstResponder:
            updated_firstResponder = await self.collection.update_one(
                {"_id": ObjectId(id)}, {"$set": data}
            )
            if updated_firstResponder:
                return True
            return False
        return False

    async def delete_firstResponder(self, id: str) -> bool:
        """Delete a student from the database"""
        student = await self.collection.find_one({"_id": ObjectId(id)})
        if student:
            await self.collection.delete_one({"_id": ObjectId(id)})
            return True
        return False
