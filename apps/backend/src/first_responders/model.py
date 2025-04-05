from pydantic import BaseModel, EmailStr, Field
from typing import Annotated, Literal
from bson import ObjectId


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


class FirstResponder(BaseModel):
    """Model of FirstResponder to manage the firstresponder data type"""

    _id: ObjectId
    fullname: str
    email: EmailStr
    designation: Literal["Paramedic", "Firefighter", "Police Officer"]
    service: str
    age: int
