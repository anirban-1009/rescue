from apps.backend.src.data_utils.baseHandler import BaseMongoHandler
from apps.backend.src.models.emergency_centres import EmergencyCentre
from typing import Optional
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from pymongo.errors import DuplicateKeyError


class EmergencyCentreHandler(BaseMongoHandler):
    """Object handling the db instance of the first responder."""

    def __init__(self):
        super().__init__()
        self.collection = self.database.get_collection("EmergencyCentre")

        # Ensure unique constraints only on necessary fields (remove email)
        self.collection.create_index(
            [("facility_name", 1), ("district", 1)], unique=True
        )

    async def add_centre(self, centre_data: dict):
        try:
            validated_data = EmergencyCentre.model_validate(centre_data)
            data_dict = validated_data.model_dump(by_alias=True, exclude_none=True)
            insert_result = await self.collection.insert_one(data_dict)
            new_centre = await self.collection.find_one(
                {"_id": insert_result.inserted_id}
            )

            if new_centre:
                new_centre["_id"] = str(new_centre["_id"])
                return EmergencyCentre.model_validate(new_centre)

        except DuplicateKeyError as e:
            raise DuplicateKeyError(f"Duplication Error: {str(e)}")

        except ValidationError as e:
            print(f"Validation Error: {e.json()}")  # Debugging
            raise ValueError(f"Validation Error: {e.json()}")

        except Exception as e:
            print(f"Database Error: {str(e)}")  # Debugging
            raise RuntimeError(f"Database Error: {str(e)}")

    async def get_emergency_centres_nearby(
        self, latitude, longitude, max_distance=5000
    ):
        """
        Fetch emergency centres within max_distance (in meters) from given coordinates.
        :param latitude: Latitude of the search location
        :param longitude: Longitude of the search location
        :param max_distance: Search radius in meters (default: 5000m)
        :return: List of emergency centres in vicinity
        """
        await self.collection.create_index([("location", "2dsphere")])

        # Use $geoNear as the first stage in the aggregation pipeline
        pipeline = [
            {
                "$geoNear": {
                    "near": {"type": "Point", "coordinates": [latitude, longitude]},
                    "distanceField": "distance",
                    "maxDistance": max_distance,  # Distance in meters
                    "spherical": True,
                }
            }
        ]

        # Execute aggregation pipeline
        results = await self.collection.aggregate(
            pipeline, maxTimeMS=60000, allowDiskUse=True
        ).to_list(None)
        return results


def ResponseModel(data: Optional[EmergencyCentre], message: str):
    return JSONResponse(
        status_code=200,
        content={"data": [data] if data else [], "code": 200, "message": message},
    )
