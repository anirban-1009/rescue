from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class FirstResponderSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    designation: str = Field(...)
    age: int = Field(..., gt=0, lte=60)
    service: str = Field()

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "johndoe@example.com",
                "designation": "Firefighter",
                "age": 35,
                "service": "Fire Department"
            }
        }


class UpdateFirstResponderModel(BaseModel):
    fullname: Optional[str]
    email: Optional[EmailStr]
    designation: Optional[str]
    age: Optional[int]
    service: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "johndoe@example.com",
                "designation": "Firefighter",
                "age": 35,
                "service": "Fire Department"
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
