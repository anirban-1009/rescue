from enum import Enum
from fastapi import HTTPException


class CentreType(str, Enum):
    AYURVEDA_DISPENSARY = "Ayurveda dispensary"
    AYUSH_DISPENSARIES = "Ayush Dispensaries"
    AYUSH_TEACHING_HOSPITAL = "Ayush Teaching Hospital"
    COMMUNITY_HEALTH_CENTER = "Community Health Center"
    DISTRICT_HOSPITAL = "District Hospital"
    FIRE_STATION = "Fire Station"
    HOMOEOPATHY_DISPENSARY = "Homoeopathy dispensary"
    HOSPITAL = "Hospital"
    M_CW_CENTER = "M&CW Center"
    MEDICAL_COLLEGES_HOSPITAL = "Medical Colleges Hospital"
    OTHERS = "Others"
    POST_PARTUM_UNIT = "Post Partum Unit"
    PRIMARY_HEALTH_CENTRE = "Primary Health Centre"
    SUB_DISTRICT_HOSPITAL = "Sub-District Hospital"
    SUBCENTRE = "SubCentre"
    UNANI_DISPENSARY = "Unani dispensary"
    URBAN_HEALTH_CENTRE_UPHC = "Urban Health Centre (UPHC)"
    URBAN_HEALTH_WELLNESS_CENTER_UHWC = "Urban health and wellness center (UHWC)"
    WOMEN_HOSPITAL = "Women Hospital"
    YOGA_NATUROPATHY_DISPENSARY = "Yoga And Naturopathy dispensary"

    @classmethod
    def validate(cls, value: str) -> str:
        """
        Validates if the given value is a valid CentreType.

        Args:
            value: The value to validate

        Returns:
            The validated value if valid

        Raises:
            HTTPException: If the value is not a valid CentreType
        """
        valid_types = [e.value for e in cls]
        if value not in valid_types:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid centre type: '{value}'. Valid types are: {valid_types}",
            )
        return value
