import pytest
from unittest.mock import AsyncMock, patch
from bson import ObjectId
from fastapi.testclient import TestClient
from fastapi import status
from pymongo.errors import DuplicateKeyError

# Import your FastAPI app - adjust the import path as needed
from src.main import app


class TestEmergencyCentreAPI:
    @pytest.fixture
    def client(self):
        """Create a FastAPI test client."""
        return TestClient(app)

    @patch(
        "src.data_utils.emergency_centres.EmergencyCentreHandler.get_emergency_centres_nearby"
    )
    def test_get_centres_near_me(self, mock_get_centres_nearby, client):
        """Test the GET /v1/emergencyCentre/getNearMe endpoint."""
        # Mock data
        mock_results = [
            {
                "_id": str(ObjectId("507f1f77bcf86cd799439011")),
                "facility_name": "City Hospital",
                "district": "Downtown",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "distance": 1200.50,
                "state": "Test State",
                "facility_type": "Hospital",
            },
        ]

        # Configure the mock method directly
        mock_get_centres_nearby.return_value = mock_results

        # Test parameters
        lat, lng = 17.4493194, 78.3749978
        max_dist, limit = 5000, 5

        # Make the request
        response = client.get(
            f"/v1/emergencyCentre/getNearMe?latitude={lat}&longitude={lng}&max_distance={max_dist}&limit={limit}",
            headers={"centre-type": "Fire Station"},
        )

        # Assert that the response is successful
        assert response.status_code == status.HTTP_200_OK

        # Assert that the handler method was called with correct parameters
        # Use ANY matcher for the centre_type parameter since it's not in our expected arguments
        mock_get_centres_nearby.assert_called_once_with(
            latitude=lat,
            longitude=lng,
            max_distance=max_dist,
            limit=limit,
            centre_type="Fire Station",
        )

        # Assert that the response data matches the expected structure with 'centres' key
        assert response.json() == {"centres": mock_results}

    @patch("src.routes.emergency_centres.get_handler")
    def test_get_centres_near_me_not_found(self, mock_get_handler, client):
        """Test the GET /v1/emergencyCentre/getNearMe endpoint when no centres are found."""
        # Configure the mock handler
        mock_handler = AsyncMock()
        mock_handler.get_emergency_centres_nearby = AsyncMock(return_value=[])
        mock_get_handler.return_value = mock_handler

        # Test parameters
        lat, lng = 90.4493194, 78.3749978

        # Make the request
        response = client.get(
            f"/v1/emergencyCentre/getNearMe?latitude={lat}&longitude={lng}",
            headers={"centre-type": "Fire Station"},
        )

        # Assert that the response is a 404 not found
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "No emergency centres found nearby" in response.json()["detail"]

    @patch("src.routes.emergency_centres.get_handler")
    def test_get_centres_near_me_invalid_header(self, mock_get_handler, client):
        """Test the GET /v1/emergencyCentre/getNearMe endpoint with invalid centre-type header."""
        # Configure the mock handler
        mock_handler = AsyncMock()
        mock_handler.get_emergency_centres_nearby = AsyncMock(return_value=[])
        mock_get_handler.return_value = mock_handler

        # Test parameters
        lat, lng = 90.4493194, 78.3749978

        # Make the request with an invalid centre-type
        response = client.get(
            f"/v1/emergencyCentre/getNearMe?latitude={lat}&longitude={lng}",
            headers={"centre-type": "Candy Store"},
        )

        # Assert the response has the expected status code and error message
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid centre type" in response.json()["detail"]

        # Ensure the handler method was never called with invalid type
        mock_handler.get_emergency_centres_nearby.assert_not_called()

    @pytest.mark.skip
    @patch("src.routes.emergency_centres.EmergencyCentreHandler")
    @patch("src.routes.emergency_centres.jsonable_encoder")
    def test_create_centre_success(
        self, mock_jsonable_encoder, mock_handler_class, client
    ):
        """Test successfully adding a new emergency centre through the POST /create endpoint."""
        # Include the required fields state and facility_type
        centre_data = {
            "facility_name": "Test Hospital",
            "district": "Test District",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "address": "123 Test St",
            "contact_no": "123-456-7890",
            "state": "Test State",
            "facility_type": "Hospital",
        }

        # Configure the jsonable_encoder mock
        mock_jsonable_encoder.return_value = centre_data

        # Configure the handler instance mock
        mock_handler_instance = AsyncMock()
        mock_handler_class.return_value = mock_handler_instance

        # Configure the add_centre method to return the created centre
        created_centre = centre_data.copy()
        created_centre["_id"] = str(ObjectId("507f1f77bcf86cd799439013"))
        mock_handler_instance.add_centre.return_value = created_centre

        # Make the request
        response = client.post(
            "/v1/emergencyCentre/create",
            json=centre_data,
        )

        # Assert that the response is successful
        assert response.status_code == status.HTTP_200_OK

        # Assert that the handler method was called with correct parameters
        mock_handler_instance.add_centre.assert_called_once_with(centre_data)

        # Check the response structure follows ResponseModel pattern
        response_data = response.json()
        assert "data" in response_data
        assert "message" in response_data
        # The data is wrapped in a list in the response
        assert response_data["data"] == [created_centre]
        assert response_data["message"] == "Centre added successfully"

    @pytest.mark.skip
    @patch("src.routes.emergency_centres.get_handler")
    def test_create_centre_validation_error(self, client):
        """Test validation error when adding a centre with missing required fields."""
        # Missing required fields: state and facility_type
        incomplete_data = {
            "facility_name": "Test Hospital",
            "district": "Test District",
            "latitude": 40.7128,
            "longitude": -74.0060,
        }

        # Make the request
        response = client.post(
            "/v1/emergencyCentre/create",
            json=incomplete_data,
        )

        # Assert that the response is a validation error
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.skip
    @patch("src.routes.emergency_centres.EmergencyCentreHandler")
    @patch("src.routes.emergency_centres.jsonable_encoder")
    @patch("src.routes.emergency_centres.get_handler")
    def test_create_centre_duplicate_error(
        self, mock_jsonable_encoder, mock_handler_class, client
    ):
        """Test handling of duplicate key errors when adding an emergency centre."""
        centre_data = {
            "facility_name": "Test Hospital",
            "district": "Test District",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "state": "Test State",
            "facility_type": "Hospital",
        }

        # Configure the jsonable_encoder mock
        mock_jsonable_encoder.return_value = centre_data

        # Configure the handler instance mock
        mock_handler_instance = AsyncMock()
        mock_handler_class.return_value = mock_handler_instance

        # Configure the add_centre method to raise DuplicateKeyError
        mock_handler_instance.add_centre.side_effect = DuplicateKeyError(
            "Duplicate key error"
        )

        # Make the request
        response = client.post(
            "/v1/emergencyCentre/create",
            json=centre_data,
        )

        # Assert response code and error details
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response_data = response.json()
        assert response_data["error"] == "Duplicate Entry"
        assert (
            "Emergency Centre with the same unique field already exists"
            in response_data["message"]
        )

    @patch("src.routes.emergency_centres.EmergencyCentreHandler")
    @patch("src.routes.emergency_centres.jsonable_encoder")
    @patch("src.routes.emergency_centres.get_handler")
    @pytest.mark.skip
    def test_create_centre_other_exception(
        self, mock_jsonable_encoder, mock_handler_class, client
    ):
        """Test handling of other exceptions when adding an emergency centre."""
        centre_data = {
            "facility_name": "Test Hospital",
            "district": "Test District",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "state": "Test State",
            "facility_type": "Hospital",
        }

        # Configure the jsonable_encoder mock
        mock_jsonable_encoder.return_value = centre_data

        # Configure the handler instance mock
        mock_handler_instance = AsyncMock()
        mock_handler_class.return_value = mock_handler_instance

        # Configure the add_centre method to raise a general Exception
        error_message = "Database connection error"
        mock_handler_instance.add_centre.side_effect = Exception(error_message)

        # Make the request
        response = client.post(
            "/v1/emergencyCentre/create",
            json=centre_data,
        )

        # Assert response code and error details
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response_data = response.json()
        assert "Error occured while creating Centre" in response_data["message"]
