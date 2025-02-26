from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_firstResponder,
)
from server.models.firstResponder import (
    ResponseModel,
    FirstResponderSchema,
)

router = APIRouter()

@router.post("/", response_description="First Responder data added into the database")
async def add_firstResponder_data(firstResponder: FirstResponderSchema = Body(...)):
    firstResponder = jsonable_encoder(firstResponder)
    new_firstResponder = await add_firstResponder(firstResponder)
    return ResponseModel(new_firstResponder, "First responder added successfully.")
