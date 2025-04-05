"""Module to create a base client for the MONGODB connection and is modular."""

import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import TypedDict
from fastapi.responses import JSONResponse


class DatabaseClass(TypedDict):
    name: str
    year: int


class BaseMongoHandler:
    def __init__(self):
        IS_CI = os.getenv("CI", "false") == "true"
        MONGO_DETAILS = os.getenv(
            "MONGODB_URL",
            "mongodb://localhost:42069/?replicaSet=test-rs"
            if IS_CI
            else "mongodb://localhost:27017",
        )

        self.client: AsyncIOMotorClient[DatabaseClass] = AsyncIOMotorClient(
            MONGO_DETAILS
        )
        self.database: AsyncIOMotorDatabase[DatabaseClass] = self.client.Rescue


def ResponseModel(data, message: str, status_code: int):
    """Response model handling data from endpoints"""
    return JSONResponse(
        status_code=status_code,
        content={
            "data": [data] if data else [],
            "code": status_code,
            "message": message,
        },
    )


def ErrorResponseModel(error: str, code: int, message: str):
    """Response model for handling error"""
    return JSONResponse(
        status_code=code, content={"error": error, "code": code, "message": message}
    )
