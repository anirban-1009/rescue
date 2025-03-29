from bson import json_util
import json
from typing import Optional

from fastapi.responses import JSONResponse
from pydantic import ValidationError
from pymongo.errors import DuplicateKeyError

from src.data_utils.baseHandler import BaseMongoHandler
from src.models.emergency_centres import EmergencyCentre


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
        self, latitude, longitude, max_distance=5000, limit=5
    ):
        # Calculate distance with Haversine formula
        pipeline = [
            # Calculate distance using a simpler formula (approximate but efficient)
            {
                "$addFields": {
                    "distance": {
                        "$multiply": [
                            111319.9,  # meters per degree (approximate)
                            {
                                "$sqrt": {
                                    "$add": [
                                        {
                                            "$pow": [
                                                {"$subtract": ["$latitude", latitude]},
                                                2,
                                            ]
                                        },
                                        {
                                            "$pow": [
                                                {
                                                    "$multiply": [
                                                        {
                                                            "$subtract": [
                                                                "$longitude",
                                                                longitude,
                                                            ]
                                                        },
                                                        {
                                                            "$cos": {
                                                                "$degreesToRadians": latitude
                                                            }
                                                        },
                                                    ]
                                                },
                                                2,
                                            ]
                                        },
                                    ]
                                }
                            },
                        ]
                    }
                }
            },
            # Filter, sort, limit - the most critical operations
            {"$match": {"distance": {"$lte": max_distance}}},
            {"$sort": {"distance": 1}},
            {"$limit": limit},
            # Handle ObjectId serialization
            {"$addFields": {"_id": {"$toString": "$_id"}}},
        ]

        results = await self.collection.aggregate(pipeline).to_list(length=None)

        # Additional safety measure: convert all results to JSON-compatible objects
        json_compatible = json.loads(json_util.dumps(results))

        return json_compatible


def ResponseModel(data: Optional[EmergencyCentre], message: str):
    return JSONResponse(
        status_code=200,
        content={"data": [data] if data else [], "code": 200, "message": message},
    )
