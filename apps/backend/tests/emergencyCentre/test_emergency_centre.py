import pytest
from unittest.mock import AsyncMock, patch
from bson import ObjectId
from fastapi.testclient import TestClient
from fastapi import status

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

    @patch("src.routes.emergency_centres.get_handler")
    @patch("src.data_utils.emergency_centres.EmergencyCentreHandler.add_centre")
    def test_create_centre_valid(self, mock_db_add_centre, mock_create_handler, client):
        """Test the POST `/v1/emergencyCentre/create` endpoint with valid data"""

        centre_data = {
            "facility_name": "Test Hospital",
            "district": "Test District",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "state": "Test State",
            "facility_type": "Hospital",
        }

        response_data = centre_data.copy()
        response_data["id"] = "mocked_id_12345"
        mock_db_add_centre.return_value = response_data

        mock_handler = AsyncMock()
        mock_create_handler.return_value = mock_handler

        response = client.post("/v1/emergencyCentre/create", json=centre_data)

        assert response.status_code == status.HTTP_201_CREATED

    @patch("src.routes.emergency_centres.get_handler")
    @patch("src.data_utils.emergency_centres.EmergencyCentreHandler.add_centre")
    def test_create_centre_invalid(
        self, mock_db_add_centre, mock_create_handler, client
    ):
        """Test the POST `/v1/emergencyCentre/create` endpoint with invalid data"""

        # Missing required fields like facility_name and state
        invalid_centre_data = {
            "district": "Test District",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "facility_type": "Hospital",
        }

        mock_handler = AsyncMock()
        mock_create_handler.return_value = mock_handler

        response = client.post("/v1/emergencyCentre/create", json=invalid_centre_data)
        assert (
            response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        )  # FastAPI validation error
        response_data = response.json()

        # Ensure the response contains validation errors for `facility_name` and `state`
        expected_error_locs = {("body", "state"), ("body", "facility_name")}

        actual_error_locs = {(tuple(err["loc"])) for err in response_data["detail"]}

        assert expected_error_locs.issubset(
            actual_error_locs
        )  # Ensure required fields are in errors

    @patch("src.routes.emergency_centres.get_handler")
    @patch("src.data_utils.emergency_centres.EmergencyCentreHandler.add_centre")
    def test_create_centre_duplicate(
        self, mock_db_add_centre, mock_create_handler, client
    ):
        """Test the POST `/v1/emergencyCentre/create` endpoint when a duplicate entry is submitted"""

        centre_data = {
            "facility_name": "Test Hospital",
            "district": "Test District",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "state": "Test State",
            "facility_type": "Hospital",
        }

        mock_handler = AsyncMock()
        mock_create_handler.return_value = mock_handler
        response = client.post("/v1/emergencyCentre/create", json=centre_data)

        # Assertions
        assert (
            response.status_code == status.HTTP_400_BAD_REQUEST
        )  # Expecting a conflict error
        response_data = response.json()
        assert response_data["message"] == "Error occured while creating Centre."
