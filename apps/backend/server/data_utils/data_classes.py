"""Module Containing the Models of the application"""

from bson.objectid import ObjectId
from pydantic import BaseModel, EmailStr
from typing import Literal


class FirstResponder(BaseModel):
    """Model of FirstResponder to manage the firstresponder data type"""

    _id: ObjectId
    fullname: str
    email: EmailStr
    designation: Literal["Paramedic", "Firefighter", "Police Officer"]
    service: str
    age: int
