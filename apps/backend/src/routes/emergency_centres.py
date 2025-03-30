from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi import Query, HTTPException, Depends, Header
from pymongo.errors import DuplicateKeyError


from src.models.emergency_centres import EmergencyCentre
from src.data_utils.emergency_centres import (
    EmergencyCentreHandler,
    ResponseModel,
)
from src.utils.error_handlers import ErrorResponseModel
from src.utils.enums import CentreType

router = APIRouter()


async def get_handler():
    from src.data_utils.emergency_centres import EmergencyCentreHandler

    return EmergencyCentreHandler()


@router.post("/create", response_description="Centre added to the database")
async def insert_centre(
    centre_data: EmergencyCentre = Body(...),
    handler: EmergencyCentreHandler = Depends(get_handler),
):
    """Insert Emergency Centre into MongoDB"""
    emergencyCentre = jsonable_encoder(centre_data)
    try:
        newEmergencyCentre: EmergencyCentre = await handler.add_centre(emergencyCentre)
        return ResponseModel(newEmergencyCentre, "Centre added successfully")

    except DuplicateKeyError as e:
        print(e)
        return ErrorResponseModel(
            error="Duplicate Entry",
            code=400,
            message="Emergency Centre with the same unique field already exists.",
        )

    except Exception as e:
        return ErrorResponseModel(
            error=e.__doc__,
            code=400,
            message="Error occured while creating Centre.",
        )


@router.get("/getNearMe", response_description="Centres near the coordinates")
async def get_centre(
    latitude: float = Query(
        ..., description="Latitude of the location", example=17.4493194
    ),
    longitude: float = Query(
        ..., description="Longitude of the location", example=78.3749978
    ),
    max_distance: int = Query(
        5000, description="Max distance in meters (default: 5000)", example=5000
    ),
    limit: int = Query(5, description="Max centres to be fetched", example=5),
    centre_type: str = Header(
        ..., description="Type of Emergency Centre to be accessed"
    ),
    handler: EmergencyCentreHandler = Depends(get_handler),
):
    """
    API to get emergency centres near the given latitude and longitude.

    Example usage:
    ```
    GET /getNearMe?latitude=19.3673515&longitude=78.7690499&max_distance=5000
    ```

    Required Headers:
    - centre-type: Type of emergency centre (Hospital, Fire Station, etc.)
    """
    try:
        # Validate the centre_type against enum values
        validated_centre_type = CentreType.validate(centre_type)

        results = await handler.get_emergency_centres_nearby(
            latitude=latitude,
            longitude=longitude,
            max_distance=max_distance,
            limit=limit,
            centre_type=validated_centre_type,
        )

        if not results:
            raise HTTPException(
                status_code=404, detail="No emergency centres found nearby."
            )

        return {"centres": results}

    except HTTPException as http_exc:
        raise http_exc  # Re-raise known HTTP exceptions

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
