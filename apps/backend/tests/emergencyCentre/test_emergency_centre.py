import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from bson import json_util, ObjectId
from pymongo.errors import DuplicateKeyError
from src.data_utils.emergency_centres import EmergencyCentreHandler


class TestEmergencyCentreHandler:
    @pytest.fixture
    def mock_emergency_handler(self):
        """Mock the EmergencyCentreHandler with a patched database connection."""
        with patch(
            "src.data_utils.emergency_centres.EmergencyCentreHandler.__init__",
            return_value=None,
        ):
            handler = EmergencyCentreHandler()
            handler.database = MagicMock()

            # Create a properly structured mock for aggregate
            aggregate_mock = MagicMock()
            to_list_mock = AsyncMock()
            aggregate_mock.return_value.to_list = to_list_mock

            handler.collection = MagicMock()
            handler.collection.aggregate = aggregate_mock
            handler.collection.insert_one = AsyncMock()
            handler.collection.find_one = AsyncMock()

            return handler

    @pytest.mark.asyncio
    async def test_get_emergency_centres_nearby(self, mock_emergency_handler):
        """Test fetching emergency centres with $geoNear aggregation."""
        # Mock data
        mock_results = [
            {
                "_id": ObjectId("507f1f77bcf86cd799439011"),
                "facility_name": "City Hospital",
                "district": "Downtown",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "distance": 1200.50,
            },
            {
                "_id": ObjectId("507f1f77bcf86cd799439012"),
                "facility_name": "Community Clinic",
                "district": "Uptown",
                "latitude": 40.7135,
                "longitude": -74.0070,
                "distance": 2500.75,
            },
        ]

        # Configure the mock aggregate method
        mock_emergency_handler.collection.aggregate.return_value.to_list.return_value = mock_results

        # Test parameters
        lat, lng, max_dist, limit = 40.7130, -74.0065, 3000, 2

        # Call the method
        results = await mock_emergency_handler.get_emergency_centres_nearby(
            latitude=lat, longitude=lng, max_distance=max_dist, limit=limit
        )

        # Verify aggregate was called correctly
        mock_emergency_handler.collection.aggregate.assert_called_once()
        pipeline = mock_emergency_handler.collection.aggregate.call_args[0][0]

        # Ensure the pipeline is structured properly
        assert any(stage.get("$addFields") for stage in pipeline), (
            "Missing $addFields stage"
        )
        assert any(stage.get("$match") for stage in pipeline), "Missing $match stage"
        assert any(stage.get("$sort") for stage in pipeline), "Missing $sort stage"
        assert any(stage.get("$limit") for stage in pipeline), "Missing $limit stage"

        # Verify JSON conversion
        expected_result = json.loads(json_util.dumps(mock_results))
        assert results == expected_result

    @pytest.mark.asyncio
    async def test_add_centre_success(self, mock_emergency_handler):
        """Test successfully adding a new emergency centre."""
        # Include the required fields state and facility_type
        centre_data = {
            "facility_name": "Test Hospital",
            "district": "Test District",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "address": "123 Test St",
            "contact_no": "123-456-7890",
            "state": "Test State",  # Added required field
            "facility_type": "Hospital",  # Added required field
        }

        # Mock EmergencyCentre.model_validate
        with patch(
            "src.models.emergency_centres.EmergencyCentre.model_validate"
        ) as mock_validate:
            # Create a mock validated model that has model_dump method
            validated_model = MagicMock()
            validated_model.model_dump.return_value = centre_data.copy()
            mock_validate.return_value = validated_model

            # Mock insert_one response
            mock_id = ObjectId("507f1f77bcf86cd799439013")
            insert_result = MagicMock()
            insert_result.inserted_id = mock_id
            mock_emergency_handler.collection.insert_one.return_value = insert_result

            # Mock find_one response
            returned_doc = centre_data.copy()
            returned_doc["_id"] = mock_id
            mock_emergency_handler.collection.find_one.return_value = returned_doc

            # Call method
            await mock_emergency_handler.add_centre(centre_data)

            # Assert insert_one and find_one calls
            mock_emergency_handler.collection.insert_one.assert_called_once()
            mock_emergency_handler.collection.find_one.assert_called_once_with(
                {"_id": mock_id}
            )

    @pytest.mark.asyncio
    async def test_add_centre_duplicate_error(self, mock_emergency_handler):
        """Test handling of duplicate key errors when adding an emergency centre."""
        centre_data = {
            "facility_name": "Test Hospital",
            "district": "Test District",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "state": "Test State",  # Added required field
            "facility_type": "Hospital",  # Added required field
        }

        # Mock model_validate to avoid validation errors
        with patch(
            "src.models.emergency_centres.EmergencyCentre.model_validate"
        ) as mock_validate:
            # Create a mock validated model that has model_dump method
            validated_model = MagicMock()
            validated_model.model_dump.return_value = centre_data.copy()
            mock_validate.return_value = validated_model

            # Configure the insert_one method to raise DuplicateKeyError
            mock_emergency_handler.collection.insert_one.side_effect = (
                DuplicateKeyError("Duplicate key error")
            )

            with pytest.raises(DuplicateKeyError):
                await mock_emergency_handler.add_centre(centre_data)

            mock_emergency_handler.collection.insert_one.assert_called_once()
