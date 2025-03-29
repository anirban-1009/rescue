from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field
from typing import Annotated, Literal, Optional

from src.data_utils.data_classes import FirstResponder


class FirstResponderSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    designation: Literal["Paramedic", "Firefighter", "Police Officer"]
    age: Annotated[int, Field(gt=0, lte=60)]
    service: str = Field()

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "johndoe@example.com",
                "designation": "Firefighter",
                "age": 35,
                "service": "Fire Department",
            }
        }


def ResponseModel(data: Optional[FirstResponder], message: str):
    return JSONResponse(
        status_code=200,
        content={"data": [data] if data else [], "code": 200, "message": message},
    )
