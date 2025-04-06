from typing import Optional
from pydantic import BaseModel, Field
from src.utils.enums import CentreType


class EmergencyCentre(BaseModel):
    state: str = Field(..., title="State Name")
    district: str = Field(..., title="District Name")
    taluka: Optional[str] = Field(None, title="Taluka or Sub-District")
    facility_name: str = Field(..., title="Name of the Facility")
    facility_type: CentreType = Field(
        ..., title="Type of Facility (Fire Station, Hospital, etc.)"
    )
    latitude: float = Field(..., title="Latitude of Facility")
    longitude: float = Field(..., title="Longitude of Facility")
    street: Optional[str] = Field(None, title="Street Address")
    landmark: Optional[str] = Field(None, title="Nearby Landmark")
    locality: Optional[str] = Field(None, title="Locality/Neighborhood")
    region_indicator: Optional[str] = Field(None, title="Urban or Rural")
    operational_status: Optional[str] = Field("Functional", title="Operational Status")
    ownership_authority: Optional[str] = Field(
        "State Government", title="Ownership Authority"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "state": "Telangana",
                "district": "Hyderabad",
                "taluka": "Serilingampally",
                "facility_name": "Madhapur Fire Station",
                "facility_type": "Fire Station",
                "latitude": 17.4493194,
                "longitude": 78.3749978,
                "street": "Hi-Tech City Road",
                "landmark": "Near Cyber Towers",
                "locality": "Madhapur",
                "region_indicator": "Urban",
                "operational_status": "Functional",
                "ownership_authority": "State Government",
            }
        }
