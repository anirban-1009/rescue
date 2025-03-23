from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from pymongo.errors import DuplicateKeyError

from apps.backend.src.data_utils.first_responder import FirstResponderHandler
from apps.backend.src.models.first_responder import (
    ResponseModel,
    ErrorResponseModel,
    FirstResponderSchema,
)
from apps.backend.src.data_utils.data_classes import FirstResponder

router = APIRouter()


@router.post(
    "/create", response_description="First Responder data added into the database"
)
async def add_firstResponder_data(firstResponder: FirstResponderSchema = Body(...)):
    firstResponder = jsonable_encoder(firstResponder)
    try:
        new_firstResponder: FirstResponder = (
            await FirstResponderHandler().add_firstResponder(firstResponder)
        )
        return ResponseModel(new_firstResponder, "First responder added successfully.")
    except DuplicateKeyError:
        return ErrorResponseModel(
            error=DuplicateKeyError.__doc__, code=400, message="Duplicate email"
        )
    except Exception as e:
        return ErrorResponseModel(
            error=e.__doc__,
            code=400,
            message="Error occured while creating FirstResponder.",
        )
