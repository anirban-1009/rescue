""" Module to create a base client for the MONGODB connection and is modular. """

import motor.motor_asyncio
from bson.objectid import ObjectId
from dataclasses import dataclass
import os

class BaseMongoHandler:

    def __init__(self):
        IS_CI = os.getenv("CI", "false") == "true"
        MONGO_DETAILS = os.getenv(
        "MONGODB_URL", 
            "mongodb://localhost:42069/?replicaSet=test-rs" if IS_CI else "mongodb://localhost:27017"
        )

        self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
        self.database = self.client.Rescue
