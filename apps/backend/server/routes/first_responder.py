from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.data_utils.first_responder import FirstResponderHandler
from server.models.first_responder import (
    ResponseModel,
    FirstResponderSchema,
)
from server.data_utils.data_classes import FirstResponder

router = APIRouter()

@router.post("/create", response_description="First Responder data added into the database")
async def add_firstResponder_data(firstResponder: FirstResponderSchema = Body(...)):
    firstResponder = jsonable_encoder(firstResponder)
    new_firstResponder:FirstResponder = await FirstResponderHandler().add_firstResponder(firstResponder)
    return ResponseModel(new_firstResponder, "First responder added successfully.", code=201)
